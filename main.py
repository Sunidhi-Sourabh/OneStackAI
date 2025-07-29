# Placeholder for main backend logic
from flask import Flask, render_template
from tools import tools_data  # 👈 import tools.py data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', tools_data=tools_data)

if __name__ == "__main__":
    app.run(debug=True)
