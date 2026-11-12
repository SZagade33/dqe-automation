with open(
    "generated_report/report.html",
    "r",
    encoding="utf-8"
) as f:
    content = f.read()

print("<table" in content)