# Placeholder for main backend logic
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to OneStackAI</h1><p>Your AI power hub is getting ready...</p>"

if __name__ == "__main__":
    app.run(debug=True)
