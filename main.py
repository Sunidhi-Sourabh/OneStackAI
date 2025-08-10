from flask import Flask, render_template
from tools import tools_data  # ✅ this should match the dictionary name in tools.py

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', tools_data=tools_data)  # ✅ this must match what Jinja expects

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)
