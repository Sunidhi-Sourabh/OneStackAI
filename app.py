    # 📦 Imports — Sorted & Cleaned
    from flask import Flask, render_template, request, redirect, url_for, jsonify, session
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_login import LoginManager, login_user, logout_user, login_required
    from flask_login import current_user
    from werkzeug.security import generate_password_hash, check_password_hash
    from models import db, User, Tool, Favorite
    from tools import tools_data  # ✅ Ensure tools.py has this dictionary

    # ⚙️ App Configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

    db.init_app(app)
    migrate = Migrate(app, db)

    # 🔐 Login Manager Setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 🧱 Create DB Tables
    with app.app_context():
        db.create_all()

    # 🔐 Login & Register Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            return render_template('login.html', error='Invalid credentials')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                error = "Passwords do not match."
                return render_template('register.html', error=error)

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

    # 🏠 Home Route with Search & Filters
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

        filters_applied = query or category_filter or pricing_filter
        return render_template('home.html',
                               tools_data=filtered_data if filters_applied else tools_data)

    # 👤 Dashboard
    @app.route('/dashboard')
    def dashboard():
        tools = Tool.query.all()
        return render_template('dashboard.html', tools=tools)

    @app.route('/favorites')
    def favorites():
        user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        tools = [Tool.query.get(f.tool_id) for f in user_favorites]
        return render_template('favorites.html', tools=tools)

    @app.route('/rate', methods=['POST'])
    def rate_tool():
        # logic here
        return jsonify({'status': 'success'})

    # ℹ️ Info Page
    @app.route('/info')
    def info():
        return render_template('info.html')

    # 🚀 Run the App
    if __name__ == '__main__':
        app.run(debug=True)
