#!./venv/bin/python
from flask import Flask, request, render_template_string

from clock import run_line

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Clock</title>
</head>
<body>
  <form action="/" method="post">
    <input type="hidden" name="who" value="helen">
    <input type="hidden" name="which" value="in">
    <button type="submit">Helen In</button>
  </form>
  <form action="/" method="post">
    <input type="hidden" name="who" value="helen">
    <input type="hidden" name="which" value="out">
    <button type="submit">Helen Out</button>
  </form>
  <form action="/" method="post">
    <input type="hidden" name="who" value="helen">
    <input type="hidden" name="which" value="report">
    <button type="submit">Helen Report</button>
  </form>

  <form action="/" method="post">
    <input type="hidden" name="who" value="amy">
    <input type="hidden" name="which" value="in">
    <button type="submit">Amy In</button>
  </form>
  <form action="/" method="post">
    <input type="hidden" name="who" value="amy">
    <input type="hidden" name="which" value="out">
    <button type="submit">Amy Out</button>
  </form>
  <form action="/" method="post">
    <input type="hidden" name="who" value="helen">
    <input type="hidden" name="which" value="report">
    <button type="submit">Amy Report</button>
  </form>

  {{ output }}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    who = request.form.get('who')
    which = request.form.get('which')

    output = ""
    if request.method == "POST":
        output = run_line(f"log {who} ; {which} ; exit")[-2]

    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == '__main__':
    app.run(debug=True)
