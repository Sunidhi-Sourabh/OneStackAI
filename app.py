# 📦 Imports — Sorted & Cleaned
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Tool, Favorite, Rating
from tools import tools_data

# ⚙️ App Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Detect DATABASE_URL from environment, else fallback to SQLite
db_url = os.environ.get('DATABASE_URL', None)

if db_url:
    # Fix old Heroku-style postgres:// to postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# 🔐 Login Manager Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 🧱 Create DB Tables + Seed tools (once)
def seed_tools_if_empty():
    if Tool.query.first():
        return
    # Flatten tools_data into Tool rows
    rows = []
    for category, tools in tools_data.items():
        for t in tools:
            rows.append(Tool(
                name=t.get('name'),
                description=t.get('description'),
                link=t.get('link'),
                pricing=t.get('pricing')
            ))
    db.session.add_all(rows)
    db.session.commit()

with app.app_context():
    db.create_all()
    seed_tools_if_empty()

# 🔐 Login & Register Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip()
        password = request.form.get('password','')
        confirm_password = request.form.get('confirm_password','')

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already exists.")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 🏠 Public Home (search/filter uses tools_data directly)
@app.route('/')
def home():
    query = (request.args.get('search') or '').lower().strip()
    category_filter = request.args.get('category', '').strip()
    pricing_filter = request.args.get('pricing', '').strip()

    filtered_data = {}
    for category, tools in tools_data.items():
        if category_filter and category != category_filter:
            continue
        matched = []
        for tool in tools:
            if query and query not in tool['name'].lower():
                continue
            if pricing_filter and tool.get('pricing','') != pricing_filter:
                continue
            matched.append(tool)
        if matched:
            filtered_data[category] = matched

    filters_applied = bool(query or category_filter or pricing_filter)
    return render_template(
        'home.html',
        tools_data=filtered_data if filters_applied else tools_data
    )

# 👤 Dashboard (DB-backed)
@app.route('/dashboard')
@login_required
def dashboard():
    tools = Tool.query.order_by(Tool.name.asc()).all()
    return render_template('dashboard.html', tools=tools)

# ⭐ Favorites toggle (AJAX)
@app.route('/favorite', methods=['POST'])
@login_required
def favorite_toggle():
    data = request.get_json(force=True)
    tool_id = int(data.get('tool_id'))
    tool = Tool.query.get_or_404(tool_id)

    fav = Favorite.query.filter_by(user_id=current_user.id, tool_id=tool.id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        db.session.add(Favorite(user_id=current_user.id, tool_id=tool.id))
        db.session.commit()
        return jsonify({'status': 'added'})

@app.route('/favorites')
@login_required
def favorites():
    favs = Favorite.query.filter_by(user_id=current_user.id).all()
    tool_ids = [f.tool_id for f in favs]
    tools = Tool.query.filter(Tool.id.in_(tool_ids)).all() if tool_ids else []
    return render_template('favorites.html', tools=tools)

# ⭐⭐ Rating (AJAX)
@app.route('/rate', methods=['POST'])
@login_required
def rate_tool():
    data = request.get_json(force=True)
    tool_id = int(data.get('tool_id'))
    value = int(data.get('value', 0))
    if value < 1 or value > 5:
        return jsonify({'status': 'error', 'message': 'Rating must be 1-5'}), 400

    tool = Tool.query.get_or_404(tool_id)
    existing = Rating.query.filter_by(user_id=current_user.id, tool_id=tool.id).first()
    if existing:
        existing.value = value
    else:
        db.session.add(Rating(user_id=current_user.id, tool_id=tool.id, value=value))
    db.session.commit()
    return jsonify({'status': 'ok', 'value': value})

# ℹ️ Info Page
@app.route('/info')
def info():
    return render_template('info.html')

# 🚀 Run the App
if __name__ == '__main__':
    app.run(debug=True)
