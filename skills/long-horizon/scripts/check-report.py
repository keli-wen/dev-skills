"""Check that a Long Horizon report fits its boxes: no label cut, no row wrapped, nothing spilling out, no sideways scroll.

Usage:
  python3 -I check-report.py <report.html> [...]   # a run's report, after writing lh-labels
  python3 -I check-report.py --stress              # the template beside this script, under worst-case content

Each page opens in headless Chrome at 375px and 1440px with ?lint; the template's lint() reports what does not fit.
Needs only Chrome or Chromium (set CHROME to its path if it is not found). Exit status: 0 fits, 1 something
does not fit, 2 no browser.
"""
import html, json, os, pathlib, re, shutil, subprocess, sys, tempfile

WIDTHS = (375, 1440)
TEMPLATE = pathlib.Path(__file__).resolve().parent.parent / "assets" / "report-template.html"

# Wordy labels at the documented limit: status values up to about 16 Latin letters
WORDY = {
    "status": {"passed": "Verified", "in-flight": "In progress", "blocked": "Needs your input",
               "failed": "Rejected", "ready": "Ready to start", "pending": "Waiting on deps"},
    "phase": {"running": "Running unattended"},
    "cut": "Bottleneck", "human": "Manual step", "new": "Newly discovered",
    "tabs": {"done": "Done when", "spec": "Spec boundary", "activity": "Decisions and activity",
             "list": "All items", "data": "Data contract"},
}


def find_chrome():
    names = [os.environ.get("CHROME", ""),
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    names += [shutil.which(n) or "" for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")]
    return next((n for n in names if n and os.path.exists(n)), None)


def block(page, name):
    return re.search(r'<script id="%s" type="application/json">(.*?)</script>' % name, page, re.S)


def put(page, name, obj):
    data = json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")
    page, n = re.subn(r'(<script id="%s" type="application/json">).*?(</script>)' % name,
                      lambda m: m.group(1) + data + m.group(2), page, flags=re.S)
    assert n == 1, name
    return page


def merge(base, extra):
    for k, v in extra.items():
        base[k] = merge(base.get(k, {}), v) if isinstance(v, dict) else v
    return base


def stress_pages(out):
    """The template's own example, pushed to the limits: one item with all three tags, a long lane name and hint,
    ISO times, a long title; once with the template's labels and once with wordy English ones."""
    page = TEMPLATE.read_text()
    labels, data = json.loads(block(page, "lh-labels").group(1)), json.loads(block(page, "lh-data").group(1))
    data["goal"].update(title="Migrate every command-line tool and its configuration files to the v2 format without breaking users",
                        updated="2026-10-12T09:30:00+08:00")
    data["log"][0]["when"] = "2026-10-12T09:30:00+08:00"
    first = data["ledger"][0]  # holds back every other item, so it is also the bottleneck
    first.update({"passes": False, "human": True, "discovered-from": "A0"})
    data["groups"][0].update(label="Infrastructure", hint="Format, fixtures and sample files for every supported platform and shell")
    paths = []
    for name, lab in (("template-labels", labels), ("wordy-labels", merge(json.loads(json.dumps(labels)), WORDY))):
        p = out / f"stress-{name}.html"
        p.write_text(put(put(page, "lh-labels", lab), "lh-data", data))
        paths.append(p)
    return paths


# Headless Chrome will not open a window narrower than 500px, so the report runs in an iframe of the exact width
# and the wrapper copies the lint result out
FRAME = """<!doctype html><body style="margin:0"><iframe id="f" src="{src}" style="width:{w}px;height:900px;border:0"></iframe>
<script>f.onload = () => {{ const p = f.contentDocument?.getElementById("lh-lint"), o = document.createElement("pre");
o.id = "lh-lint"; o.textContent = p ? p.textContent : ""; document.body.append(o) }}</script>"""


def lint(chrome, path, width, tmp):
    frame = tmp / f"frame-{width}.html"
    frame.write_text(FRAME.format(src=html.escape(path.resolve().as_uri() + "?lint"), w=width))
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           "--allow-file-access-from-files", f"--user-data-dir={tmp / 'profile'}", f"--window-size={width + 100},1000",
           "--virtual-time-budget=3000", "--dump-dom", frame.as_uri()]
    dom = subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout
    m = re.search(r'<pre id="lh-lint">(.+?)</pre>', dom, re.S)
    if not m:
        return [{"kind": "no lint output", "where": "is this report built from the current template?"}]
    result = json.loads(html.unescape(m.group(1)))
    assert result["width"] == width, f"lint ran at {result['width']}px, not {width}px"
    return result["problems"]


def main(args):
    chrome = find_chrome()
    if not chrome:
        print("No Chrome or Chromium found; set CHROME to its path.", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        pages = stress_pages(tmp) if args == ["--stress"] else [pathlib.Path(a) for a in args]
        if not pages:
            print(__doc__.strip())
            return 2
        bad = 0
        for page in pages:
            for width in WIDTHS:
                problems = lint(chrome, page, width, tmp)
                bad += len(problems)
                print(f"{'ok  ' if not problems else 'FAIL'} {page.name} @ {width}px")
                for p in problems:
                    print(f"     {p['kind']}: {p['where']}")
        return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
