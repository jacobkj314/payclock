#!./venv/bin/python
from flask import Flask, request, render_template_string

from clock import run_line
import config
app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Clock</title>

  <style>
    body {
      font-size: 2em;
    }

    button, input, select, textarea {
     font-size: inherit;
    }

    table, th, td {
      border: 1px solid black;
      border-collapse: collapse; /* ensures borders don't double up */
      padding: 8px;
    }

  </style>

</head>
<body>


  <h1> {{ name }} Clock Tracker </h1>

  <table>
  {% for whoitem in who %}
    <tr>
    {% for whichitem in which %}
      <td>
        <form action="/" method="post" style="display:inline">
          <input type="hidden" name="who" value="{{ whoitem }}">
          <input type="hidden" name="which" value="{{ whichitem }}">
          <button type="submit">{{ whoitem }} {{ whichitem }}</button>
        </form>
      </td>
    {% endfor %}
    <tr/>
  {% endfor %}
  </table>
  
  <pre>
{{ output }}
  </pre>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    who = request.form.get('who')
    which = request.form.get('which')

    output = ""
    if request.method == "POST":
        output = run_line(f"log {who} ; {which} ; exit", print = lambda *args, **kwargs : None)[-2]

    return render_template_string(HTML_TEMPLATE, output=output, who=config.who, which=config.which, name=config.name)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
