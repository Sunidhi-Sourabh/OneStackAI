from flask import Flask, render_template
from tools import tools_data  # ✅ this should match the dictionary name in tools.py

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', tools_data=tools_data)  # ✅ this must match what Jinja expects

if __name__ == '__main__':
    app.run(debug=True)
