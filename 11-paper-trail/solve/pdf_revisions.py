# Paper Trail - a PDF saved with "incremental updates" still contains the older version inside it
import subprocess, re

data = open("../files/report.pdf", "rb").read()
eofs = [m.end() for m in re.finditer(rb"%%EOF\s*", data)]
print(f"found {len(eofs)} revisions (each one ends with %%EOF)")

for n, end in enumerate(eofs, 1):
    name = f"revision_{n}.pdf"
    open(name, "wb").write(data[:end])           # everything up to this %%EOF = the file as it was then
    print(f"\n===== {name} =====")
    print(subprocess.run(["pdftotext", "-layout", name, "-"], capture_output=True, text=True).stdout)
    info = subprocess.run(["pdfinfo", name], capture_output=True, text=True).stdout
    print("\n".join(l for l in info.splitlines() if l.split(":")[0] in ("Title", "Author", "Subject", "Keywords")))

print("\n===== the later revision also adds a hidden annotation =====")
for m in re.finditer(rb"/Subtype /Text[^>]*?/Contents \(([^)]*)\)", data):
    print("annotation text:", m.group(1).decode())
