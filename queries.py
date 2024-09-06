# queries.py

from models import db, User
from werkzeug.security import generate_password_hash

def register_user(name, email, password, confirm_password):
    if password != confirm_password:
        return False, "Las contraseñas no coinciden."

    if User.query.filter_by(email=email).first():
        return False, "El correo electrónico ya está registrado."

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(name=name, email=email, password_hash=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, "Error al registrar el usuario. Intenta nuevamente más tarde."
