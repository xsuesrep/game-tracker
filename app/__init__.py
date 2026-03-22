from flask import Flask, render_template, request, redirect
from .models import db, User, Game, Performance
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

login_manager = LoginManager()
login_manager.login_view = "login"


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    # โหลด user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # =========================
    # 🔥 หน้าแรก (redirect)
    # =========================
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect("/home")
        return redirect("/login")


    # =========================
    # 🏠 HOME + SEARCH
    # =========================
    @app.route("/home")
    @login_required
    def home():
        keyword = request.args.get("q")

        if keyword:
            games = Game.query.filter(
                Game.user_id == current_user.id,
                Game.name.ilike(f"%{keyword}%")
            ).all()
        else:
            games = Game.query.filter_by(user_id=current_user.id).all()

        return render_template("home.html", games=games)


    # =========================
    # ➕ ADD GAME
    # =========================
    @app.route("/add-game", methods=["GET", "POST"])
    @login_required
    def add_game():
        if request.method == "POST":
            name = request.form.get("name")
            genre = request.form.get("genre")

       
            image_url = request.form.get("image_url")
           
            new_game = Game(
               name=name,
               genre=genre,
               image_url=image_url,
               user_id=current_user.id
        )

            db.session.add(new_game)
            db.session.commit()

            return redirect("/home")

        return render_template("add_game.html")


    # =========================
    # 🔐 LOGIN
    # =========================
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect("/home")

        return render_template("login.html")


    # =========================
    # 🚪 LOGOUT
    # =========================
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/login")


    # =========================
    # 📝 REGISTER
    # =========================
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            # 🔥 กัน user ซ้ำ
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return "Username already exists!"

            hashed_pw = generate_password_hash(password)

            new_user = User(username=username, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()

            return redirect("/login")

        return render_template("register.html")


    # =========================
    # 🎮 ADD PERFORMANCE
    # =========================
    @app.route("/add-performance/<int:game_id>", methods=["GET", "POST"])
    @login_required
    def add_performance(game_id):
        if request.method == "POST":
            graphics = request.form.get("graphics")
            fps = request.form.get("fps")
            resolution = request.form.get("resolution")

            new_perf = Performance(
                graphics_setting=graphics,
                fps=int(fps),
                resolution=resolution,
                game_id=game_id
            )

            db.session.add(new_perf)
            db.session.commit()

            return redirect("/home")

        return render_template("add_performance.html", game_id=game_id)


    # =========================
    # ❌ DELETE GAME
    # =========================
    @app.route("/delete-game/<int:id>")
    @login_required
    def delete_game(id):
        game = Game.query.get_or_404(id)

        if game.user_id != current_user.id:
            return redirect("/home")

        db.session.delete(game)
        db.session.commit()

        return redirect("/home")


    # =========================
    # ✏️ EDIT GAME
    # =========================
    @app.route("/edit-game/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_game(id):
        game = Game.query.get_or_404(id)

        if game.user_id != current_user.id:
            return redirect("/home")

        if request.method == "POST":
            game.name = request.form.get("name")
            game.genre = request.form.get("genre")
            game.rating = int(request.form.get("rating"))
            game.platform = request.form.get("platform")
            game.status = request.form.get("status")
            game.note = request.form.get("note")

            db.session.commit()

            return redirect("/home")

        return render_template("edit_game.html", game=game)


    # =========================
    # 🎮 GAME DETAIL
    # =========================
    @app.route("/game/<int:id>")
    @login_required
    def game_detail(id):
        game = Game.query.get_or_404(id)
        return render_template("game_detail.html", game=game)


    # =========================
    # 👤 PROFILE
    # =========================
    @app.route("/profile")
    @login_required
    def profile():
        games = Game.query.filter_by(user_id=current_user.id).all()
        return render_template("profile.html", games=games)


    return app