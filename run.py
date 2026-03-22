from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # 👇 เพิ่ม user test
    if not User.query.filter_by(username="admin").first():
        user = User(
            username="admin",
            password=generate_password_hash("1234")
        )
        db.session.add(user)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)