from flask import Flask, render_template
from flask import Flask, render_template, request

from tools import tools_data  # ✅ this should match the dictionary name in tools.py

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    pricing_filter = request.args.get('pricing', '')

    filtered_data = {}

    for category, tools in tools_data.items():
        if category_filter and category != category_filter:
            continue

        matched = []
        for tool in tools:
            if query and query not in tool['name'].lower():
                continue
            if pricing_filter and tool['pricing'] != pricing_filter:
                continue
            matched.append(tool)

        if matched:
            filtered_data[category] = matched

    return render_template('home.html', tools_data=filtered_data if query or category_filter or pricing_filter else tools_data)

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)
