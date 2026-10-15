#!/usr/bin/env python3
"""Preflight for a client release review — the client counterpart of prep_drift.py.

One command, no model.  For every release tag of a client lineage that has no page, it
establishes identity, picks the nearest audited ancestor as the base, and writes the
evidence a reviewer is briefed with, so that no reviewer re-derives any of it:

  brief-<lineage>-<tag>.txt   identity, base, what changed, what to read first
  <tag>.shipping.diff         shipping-code diff base -> tag (tests, docs, assets excluded)
  <tag>.config.diff           manifests, dependency catalogue, build scripts, backup and network rules
  <tag>.sweep.tsv             WHOLE-TREE sink sweep at the tag, each hit NEW or CARRIED against the
                              ledger of the base page (see below) — never only the changed hunks
  <tag>.native.tsv            (android) every native library in the released APK, sha256, and whether
                              its bytes changed since the base release — a changed one needs §4b step 5

Efficiency comes from two ledgers kept beside the pages, written by --record after a page is
published and never by a reviewer:

  client/<lineage>/sweep/<tag>.tsv    the swept hits that page covered, by fingerprint
  client/<lineage>/native/<tag>.tsv   the native libraries that page checked, by sha256

A fingerprint is the hit line plus three lines either side, whitespace-normalised, so a line
whose surroundings changed comes back NEW even when the line itself did not.  CARRIED means
"read in context at <base tag>", not "safe": the reviewer still owns every hit, and the brief
lists CARRIED hits in full so the whole-tree sweep stays whole.

Usage:
  tools/prep_client.py --lineage teemoon-android --out <scratch>/client-prep
  tools/prep_client.py --lineage teemoon-android --tag v1.0.4-3910 --out <dir>     # one tag
  tools/prep_client.py --lineage teemoon-android --record v1.0.4-3910 --from <dir>  # after publish

Exit 0: nothing unaudited.  Exit 1: briefs written.  Exit 2: no network / identity failure.
Never writes a page (README: nothing in tools/ writes a page).
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(tempfile.gettempdir(), "teemoon-client-src")

LINEAGES = {
    "teemoon-ios": {
        "repo": "teemoonai/teemoon-ios",
        "tag": r"^v\d+\.\d+\.\d+$",                       # App Store tags; tf/* are TestFlight
        "exclude": [":(exclude)*Tests*", ":(exclude)*.md", ":(exclude)*.png", ":(exclude)*.xcassets*",
                    # the public squash drops these; a dev-vs-public diff must not count them as shipping code
                    ":(exclude)docs/*", ":(exclude)tools/*", ":(exclude)scripts/*", ":(exclude)design/*",
                    ":(exclude)Playgrounds/*", ":(exclude)conformance/*", ":(exclude).github/*", ":(exclude)assets/*",
                    ":(exclude)Makefile", ":(exclude)CLAUDE.md"],
        "config": ["teemoon/Info.plist", "teemoon/teemoon.entitlements", "*Package.resolved",
                   "Packages/*/Package.swift", "*project.pbxproj"],
        "code": r"\.(swift|m|h|c|cpp|rs)$",
        "skip": r"(Tests?/|UITests/|\.build/|Playgrounds/|docs/|tools/|scripts/|design/)",
        "sinks": {
            "log": r"\b(Logger|os_log|NSLog|print|debugPrint|dump)\s*\(|\blogger\.\w+\(",
            "store": r"UserDefaults|FileManager|\.write\(to:|createFile|Keychain|SecItem",
            "net": r"URLSession|URLRequest|https?://|setValue\([^)]*forHTTPHeaderField|Authorization|Bearer",
            "pasteboard": r"UIPasteboard|NSPasteboard",
            "render": r"AsyncImage|WKWebView|ImageLoader|attachmentLoader|openURL",
            "entry": r"AppIntent|NSUserActivity|onOpenURL|CSSearchable",
        },
    },
    "teemoon-android": {
        "repo": "teemoonai/teemoon-android",
        "tag": r"^v\d+\.\d+\.\d+(-\d+)?$",                # Play-store releases only (RELEASE_PLAN §6)
        "exclude": [":(exclude)**/src/test/**", ":(exclude)**/src/androidTest/**", ":(exclude)*.md",
                    ":(exclude)*.png", ":(exclude)*.webp", ":(exclude)docs/**", ":(exclude)tools/**",
                    ":(exclude).github/**", ":(exclude)**/jniLibs/**",
                    ":(exclude)conformance/**"],   # test-only (no src/main, not in the dex at 3910); a build change shows in config.diff
        "config": ["*AndroidManifest.xml", "*/res/xml/*.xml", "gradle/libs.versions.toml", "*build.gradle.kts",
                   "settings.gradle.kts", "gradle.properties", "gradle/wrapper/gradle-wrapper.properties",
                   "*proguard-rules.pro", "*consumer-rules.pro"],
        "code": r"\.(kt|java|kts|xml|cpp|c|h|rs)$",
        "skip": r"(/src/test/|/src/androidTest/|^docs/|^tools/|^\.github/|/build/|^conformance/)",
        "sinks": {
            "log": r"\bLog\.[vdiwe]\(|\bLog\.wtf\(|println\(|printStackTrace\(|System\.(out|err)|Timber\.|"
                   r"\w*Trace\.\w+\(|debugText\(|LastRequestDebug",
            "store": r"SharedPreferences|getSharedPreferences|DataStore|openFileOutput|FileOutputStream|"
                     r"\.writeText\(|\.writeBytes\(|\.appendText\(|cacheDir|getExternalFilesDir|externalCacheDir|"
                     r"KeyStore|EncryptedFile|@Entity|Room\.",
            "net": r"OkHttpClient|Request\.Builder|HttpURLConnection|openConnection|\.url\(|https?://|"
                   r"[\"']Authorization[\"']|Bearer |addHeader\(|\.header\(|WebSocket|DownloadManager",
            "pasteboard": r"ClipboardManager|setPrimaryClip|ClipData|LocalClipboardManager|setText\(AnnotatedString",
            "render": r"AsyncImage|ImageRequest|coil|ImageLoader|WebView|loadUrl|evaluateJavascript|"
                      r"imageTransformer|LocalUriHandler|openUri\(|ACTION_VIEW",
            "entry": r"<intent-filter|exported=\"true\"|ACTION_SEND|ContentProvider|FileProvider|"
                     r"BroadcastReceiver|PendingIntent|Notification\w*Builder|setContentText|AppWidget|"
                     r"getStringExtra|intent\.extras|UiTestSeeding",
            "native": r"System\.loadLibrary|external fun |JNIEXPORT|dlopen",
        },
    },
}

def sh(*args, cwd=None, check=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(args)}: {r.stderr.strip()[:400]}")
    return r.stdout

def gh_json(path):
    """GitHub API through the gh CLI when it is logged in (a private repo needs it), else anonymous."""
    if shutil.which("gh"):
        r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
        if r.returncode == 0:
            return json.loads(r.stdout)
    import urllib.request
    req = urllib.request.Request("https://api.github.com/" + path, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as f:
        return json.load(f)

def clone(L):
    d = os.path.join(CACHE, L["repo"].replace("/", "__"))
    if not os.path.isdir(d):
        os.makedirs(CACHE, exist_ok=True)
        sh("gh", "repo", "clone", L["repo"], d, "--", "-q") if shutil.which("gh") else \
            sh("git", "clone", "-q", f"https://github.com/{L['repo']}.git", d)
    sh("git", "fetch", "-q", "--tags", "--force", "origin", cwd=d)
    return d

def pages(lineage):
    d = os.path.join(ROOT, "client", lineage)
    out = {}
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        m = re.match(r"^((?:v|tf-)[\d.]+(?:-\d+)?)-([0-9a-f]{7,})\.md$", f) or re.match(r"^(dev-[0-9a-f]{7})\.md$", f)
        if not m:
            continue   # dev-<sha>.md / tf-<ver>-<build>-<sha>.md: candidate pages; usable as a base by --ref runs only (release runs filter to tags)
        text = open(os.path.join(d, f), encoding="utf-8").read()
        sha = re.search(r"commit `([0-9a-f]{40})`", text)
        out[m.group(1)] = {"file": f, "sha": sha.group(1) if sha else None,
                           "skeleton": "review in progress" in text}
    return out

def release_tags(L, repo_dir):
    rx = re.compile(L["tag"])
    out = {}
    for line in sh("git", "for-each-ref", "--format=%(refname:short) %(*objectname)%(objectname)", "refs/tags", cwd=repo_dir).split():
        pass
    for name in sh("git", "tag", cwd=repo_dir).split():
        if rx.match(name):
            out[name] = sh("git", "rev-parse", f"{name}^{{commit}}", cwd=repo_dir).strip()
    return out

def base_for(tag_sha, audited, repo_dir):
    """Nearest audited commit that is an ancestor of the target; else the most recent audited one."""
    best = None
    for tag, p in audited.items():
        if not p["sha"] or p["skeleton"]:
            continue
        anc = subprocess.run(["git", "merge-base", "--is-ancestor", p["sha"], tag_sha], cwd=repo_dir).returncode == 0
        n = int(sh("git", "rev-list", "--count", f"{p['sha']}..{tag_sha}", cwd=repo_dir).strip() or 0)
        key = (0 if anc else 1, n)
        if best is None or key < best[0]:
            best = (key, tag, p)
    return (best[1], best[2]) if best else (None, None)

def tree_files(repo_dir, sha, L):
    names = sh("git", "ls-tree", "-r", "--name-only", sha, cwd=repo_dir).splitlines()
    return [n for n in names if re.search(L["code"], n) and not re.search(L["skip"], n)]

def fingerprint(path, lines, i):
    ctx = " ".join(" ".join(l.split()) for l in lines[max(0, i - 3): i + 4])
    return hashlib.sha1(f"{path}\0{ctx}".encode()).hexdigest()[:16]

def sweep(repo_dir, sha, L):
    rx = {k: re.compile(v) for k, v in L["sinks"].items()}
    hits = []
    for path in tree_files(repo_dir, sha, L):
        try:
            text = sh("git", "show", f"{sha}:{path}", cwd=repo_dir)
        except RuntimeError:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines):
            s = line.strip()
            if not s or s.startswith(("//", "*", "/*", "#", "<!--")):
                continue
            kinds = [k for k, r in rx.items() if r.search(line)]
            if kinds:
                hits.append({"fp": fingerprint(path, lines, i), "path": path, "line": i + 1,
                             "kinds": ",".join(kinds), "text": s[:160]})
    return hits

def ledger(lineage, kind, tag):
    p = os.path.join(ROOT, "client", lineage, kind, f"{tag}.tsv") if tag else None
    if not p or not os.path.isfile(p):
        return {}
    rows = [l.rstrip("\n").split("\t") for l in open(p, encoding="utf-8") if not l.startswith("#")]
    return {r[0]: r for r in rows if r}

def release_info(L, tag, outdir, local_apk=None):
    """Release notes verdict and the APK's bytes, when the release carries an APK."""
    if local_apk:
        info = {"release": None, "apk": {"name": os.path.basename(local_apk), "path": local_apk,
                "sha256": hashlib.sha256(open(local_apk, "rb").read()).hexdigest()}}
        signer = find_tool("apksigner")
        if signer:
            certs = subprocess.run([signer, "verify", "--print-certs", local_apk], capture_output=True, text=True).stdout
            m = re.search(r"certificate SHA-256 digest: ([0-9a-f]+)", certs)
            info["apk"]["signer_sha256"] = m.group(1) if m else None
        return info
    try:
        rel = gh_json(f"repos/{L['repo']}/releases/tags/{tag}")
    except Exception:
        return {"release": None}
    body = rel.get("body") or ""
    v = re.search(r"\*\*(verified|FAILED|mismatch)\*\*", body, re.I)
    info = {"release": rel.get("html_url"), "published": rel.get("published_at"),
            "reproducibility": v.group(1) if v else "not stated", "apk": None}
    apk = next((a for a in rel.get("assets", []) if a["name"].endswith(".apk")), None)
    if apk:
        dst = os.path.join(outdir, apk["name"])
        if not os.path.isfile(dst):
            sh("gh", "release", "download", tag, "-R", L["repo"], "-p", apk["name"], "-D", outdir, "--clobber")
        info["apk"] = {"name": apk["name"], "sha256": hashlib.sha256(open(dst, "rb").read()).hexdigest(), "path": dst}
        signer = find_tool("apksigner")
        if signer:
            certs = subprocess.run([signer, "verify", "--print-certs", dst], capture_output=True, text=True).stdout
            m = re.search(r"certificate SHA-256 digest: ([0-9a-f]+)", certs)
            info["apk"]["signer_sha256"] = m.group(1) if m else None
    return info

def find_tool(name):
    if shutil.which(name):
        return shutil.which(name)
    for sdk in [os.environ.get("ANDROID_HOME", ""), "/opt/homebrew/share/android-commandlinetools",
                os.path.expanduser("~/Library/Android/sdk")]:
        bt = os.path.join(sdk, "build-tools")
        if os.path.isdir(bt):
            for v in sorted(os.listdir(bt), reverse=True):
                p = os.path.join(bt, v, name)
                if os.path.isfile(p):
                    return p
    return None

def native_inventory(apk_path):
    out = []
    with zipfile.ZipFile(apk_path) as z:
        for n in sorted(z.namelist()):
            if n.startswith("lib/") and n.endswith(".so"):
                out.append((n, hashlib.sha256(z.read(n)).hexdigest()))
    return out

def write_tsv(path, header, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# " + "\t".join(header) + "\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")

def code_equivalent(repo_dir, a, b, L):
    """Non-comment, non-blank code lines that differ between two trees (publish-time stripping touches comments only)."""
    d = sh("git", "diff", "-U0", a, b, "--", "*.kt", "*.kts", "*.java", "*.xml", "*.toml", "*.properties", "*.swift",
           *L["exclude"], cwd=repo_dir)
    rx = re.compile(r"^[+-]\s*(//|\*|/\*|<!--|#|$)")
    return [l for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---")) and not rx.match(l)]

def prep(lineage, L, tag, sha, audited, repo_dir, out, local_apk=None, forced_base=None, base_ref=None):
    base_tag, base = forced_base or base_for(sha, audited, repo_dir)
    diff_from = base["sha"] if base else None
    if base and base_ref:
        diff_from = sh("git", "rev-parse", f"{base_ref}^{{commit}}", cwd=repo_dir).strip()
        extra = code_equivalent(repo_dir, base["sha"], diff_from, L)
        if extra:
            raise RuntimeError(f"--base-ref {base_ref} is not code-identical to {base_tag}: {len(extra)} code lines differ")
    kind = "NEW" if not base else ("DELTA" if subprocess.run(
        ["git", "merge-base", "--is-ancestor", base["sha"], sha], cwd=repo_dir).returncode == 0 else "SIBLING")
    tree = sh("git", "rev-parse", f"{sha}^{{tree}}", cwd=repo_dir).strip()
    files = tree_files(repo_dir, sha, L)
    loc = sum(len(sh("git", "show", f"{sha}:{p}", cwd=repo_dir).splitlines()) for p in files)
    lines = [f"CLIENT BRIEF — {lineage} {tag}", "",
             f"identity     tag {tag} -> commit {sha} (tree {tree})",
             f"repo         https://github.com/{L['repo']}",
             f"kind         {kind}" + (f" from {base_tag} @ {base['sha']} (page client/{lineage}/{base['file']})" if base else
                                         " — no audited release in this lineage: full review"),
             f"page path    client/{lineage}/{tag if tag.startswith('dev-') else tag + '-' + sha[:7]}.md",
             f"shipping     {len(files)} code files, {loc} lines (tests, docs, tools excluded)"]
    rel = release_info(L, tag, out, local_apk)
    if rel.get("release"):
        lines.append(f"release      {rel['release']} published {rel['published']}; reproducibility in notes: {rel['reproducibility']}")
    if rel.get("apk"):
        a = rel["apk"]
        lines.append(f"apk          {a['name']} sha256 {a['sha256']} signer {a.get('signer_sha256') or 'apksigner not found'}")
    lines.append("")
    if base:
        if diff_from != base["sha"]:
            lines.append(f"diff base      {diff_from} — code-identical to {base_tag} @ {base['sha'][:7]} (comments aside, checked)")
        diff = sh("git", "diff", diff_from, sha, "--", ".", *L["exclude"], cwd=repo_dir)
        open(os.path.join(out, f"{tag}.shipping.diff"), "w").write(diff)
        stat = sh("git", "diff", "--shortstat", diff_from, sha, "--", ".", *L["exclude"], cwd=repo_dir).strip()
        lines.append(f"shipping diff  {tag}.shipping.diff — {stat or 'EMPTY: zero shipping-code change'}")
    cfg = sh("git", "diff", diff_from if base else sh("git", "hash-object", "-t", "tree", "/dev/null", cwd=repo_dir).strip(),
             sha, "--", *L["config"], cwd=repo_dir)
    open(os.path.join(out, f"{tag}.config.diff"), "w").write(cfg)
    lines.append(f"config diff    {tag}.config.diff — {len(cfg.splitlines())} lines" + ("" if base else " (whole files: no base)"))
    hits = sweep(repo_dir, sha, L)
    prev = ledger(lineage, "sweep", base_tag)
    new = [h for h in hits if h["fp"] not in prev]
    write_tsv(os.path.join(out, f"{tag}.sweep.tsv"), ["status", "fingerprint", "path:line", "kinds", "text"],
              [("NEW" if h["fp"] not in prev else f"CARRIED({base_tag})", h["fp"], f"{h['path']}:{h['line']}",
                h["kinds"], h["text"]) for h in sorted(hits, key=lambda h: (h["fp"] in prev, h["path"], h["line"]))])
    by = {}
    for h in new:
        by[h["kinds"].split(",")[0]] = by.get(h["kinds"].split(",")[0], 0) + 1
    lines.append(f"sink sweep     {tag}.sweep.tsv — {len(hits)} hits in the whole tree; {len(new)} NEW"
                 f" ({', '.join(f'{k} {v}' for k, v in sorted(by.items()))}), {len(hits) - len(new)} CARRIED from {base_tag or '-'}")
    if rel.get("apk"):
        inv = native_inventory(rel["apk"]["path"])
        pn = ledger(lineage, "native", base_tag)
        known = {r[1] for r in pn.values() if len(r) > 1}
        rows = [(n, h, "CHECKED(" + base_tag + ")" if h in known else "CHECK") for n, h in inv]
        write_tsv(os.path.join(out, f"{tag}.native.tsv"), ["lib", "sha256", "status"], rows)
        lines.append(f"native libs    {tag}.native.tsv — {len(inv)} libraries; {sum(r[2] == 'CHECK' for r in rows)} need the "
                     "binary capability check (new bytes since the base page)")
    lines += ["", "Read order: this brief -> config diff -> shipping diff (every hunk) -> sweep NEW rows (each adjudicated)",
              "-> sweep CARRIED rows (skim in context; a carried line is not a cleared line) -> the base page's findings."]
    open(os.path.join(out, f"brief-{lineage}-{tag}.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join("  " + l for l in lines[:12] if l))
    return {"tag": tag, "sha": sha, "kind": kind, "base": base_tag, "new_hits": len(new)}

def record(lineage, tag, src):
    """After the page is published: the swept hits and checked libraries become the next base's ledger."""
    for kind, fname, keep in (("sweep", f"{tag}.sweep.tsv", lambda r: (r[1], r[2], r[3])),
                              ("native", f"{tag}.native.tsv", lambda r: (r[0], r[1]))):
        p = os.path.join(src, fname)
        if not os.path.isfile(p):
            continue
        rows = [l.rstrip("\n").split("\t") for l in open(p, encoding="utf-8") if not l.startswith("#")]
        d = os.path.join(ROOT, "client", lineage, kind)
        os.makedirs(d, exist_ok=True)
        hdr = ["fingerprint", "path:line", "kinds"] if kind == "sweep" else ["lib", "sha256"]
        write_tsv(os.path.join(d, f"{tag}.tsv"), hdr, [keep(r) for r in rows])
        print(f"recorded client/{lineage}/{kind}/{tag}.tsv ({len(rows)} rows)")

def candidate(a, L):
    """A pre-release dev commit: same brief, labelled dev-<sha>, against the most recent audited page.
    The audited commit must be readable from the checkout (fetch the public repo into it as a remote): a dev tree
    and the public tree share no history, so the diff is tree-to-tree and carries publish-time edits as noise."""
    repo_dir = a.repo_dir
    sha = sh("git", "rev-parse", f"{a.ref}^{{commit}}", cwd=repo_dir).strip()
    have = pages(a.lineage)
    usable = {t: p for t, p in have.items() if p["sha"] and not p["skeleton"] and
              subprocess.run(["git", "cat-file", "-e", p["sha"] + "^{commit}"], cwd=repo_dir).returncode == 0}
    if not usable:
        print("no audited commit is readable from this checkout: git fetch the public repo into it", file=sys.stderr)
        return 2
    newest = max(usable.items(), key=lambda kv: int(sh("git", "show", "-s", "--format=%ct", kv[1]["sha"], cwd=repo_dir)))
    if a.base:  # a public tag assembled from an OLDER dev page than the newest one (3915 published after 3916 was reviewed)
        if a.base not in usable:
            print(f"--base {a.base}: no such audited page readable from this checkout", file=sys.stderr); return 2
        newest = (a.base, usable[a.base])
    label = f"dev-{sha[:7]}"
    print(f"{a.lineage} {label} (candidate, base {newest[0]}):")
    r = prep(a.lineage, L, label, sha, usable, repo_dir, a.out, a.apk, forced_base=newest, base_ref=a.base_ref)
    r["kind"] = "CANDIDATE " + r["kind"]
    json.dump([r], open(os.path.join(a.out, "summary.json"), "w"), indent=2)
    return 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lineage", choices=sorted(LINEAGES), default="teemoon-android")
    ap.add_argument("--tag")
    ap.add_argument("--out", default=os.path.join(tempfile.gettempdir(), "client-prep"))
    ap.add_argument("--repo-dir", help="a local checkout to read instead of the GitHub clone (a dev candidate)")
    ap.add_argument("--ref", help="with --repo-dir: an untagged commit to brief, labelled dev-<short sha>")
    ap.add_argument("--base-ref", help="with --ref: the dev commit the base page's public tree was assembled from; "
                    "diffs start there, after a check that it is code-identical to the audited commit (comments aside)")
    ap.add_argument("--base", help="with --ref: the audited page tag to diff from, instead of the newest readable one")
    ap.add_argument("--apk", help="a locally built APK for the candidate (no GitHub release to download)")
    ap.add_argument("--record")
    ap.add_argument("--from", dest="src")
    a = ap.parse_args()
    if a.record:
        return record(a.lineage, a.record, a.src or a.out) or 0
    L = LINEAGES[a.lineage]
    os.makedirs(a.out, exist_ok=True)
    if a.repo_dir and a.ref:
        return candidate(a, L)
    try:
        repo_dir = clone(L)
    except Exception as e:
        print(f"cannot reach {L['repo']}: {e}", file=sys.stderr)
        return 2
    live, have = release_tags(L, repo_dir), pages(a.lineage)
    todo = [a.tag] if a.tag else [t for t in sorted(live) if t not in have or have[t]["sha"] != live[t]]
    if not todo:
        print(f"{a.lineage}: every release tag has a page. Nothing to commission.")
        return 0
    audited = {t: p for t, p in have.items() if t in live and p["sha"] == live[t]}
    results = []
    for t in todo:
        if t not in live:
            print(f"{t}: not a release tag of {L['repo']}", file=sys.stderr)
            return 2
        print(f"{a.lineage} {t}:")
        results.append(prep(a.lineage, L, t, live[t], audited, repo_dir, a.out))
    json.dump(results, open(os.path.join(a.out, "summary.json"), "w"), indent=2)
    print(f"\n{len(results)} unaudited tag(s); briefs in {a.out}")
    return 1

if __name__ == "__main__":
    sys.exit(main())
