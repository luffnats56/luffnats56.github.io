"""Print the portfolio HTML to PDF with headless Chrome (temp profile, no conflicts)."""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "index.html")
PDF = os.path.join(HERE, "portfolio-karina.pdf")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

tmp = tempfile.mkdtemp(prefix="chrome_print_")
url = "file:///" + HTML.replace("\\", "/") + "?r=%d" % os.path.getsize(HTML)
cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run",
       "--user-data-dir=" + tmp, "--no-pdf-header-footer", "--print-to-pdf=" + PDF,
       "--print-to-pdf-paper-size=A4", "--virtual-time-budget=12000", url]
print("printing:", pdf if False else PDF)
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc", r.returncode)
if r.stderr:
    print(r.stderr[-800:])
print("exists:", os.path.exists(PDF), os.path.getsize(PDF) if os.path.exists(PDF) else 0)

try:
    import fitz
    d = fitz.open(PDF)
    print("pages:", d.page_count)
    for i in range(min(d.page_count, 8)):
        imgs = len(d[i].get_images(full=True))
        txt = d[i].get_text().strip().replace("\n", " ")[:70]
        print("  p%d images=%d | %s" % (i + 1, imgs, txt))
except Exception as e:
    print("verify skipped:", repr(e)[:120])
