from flask import current_app, request
from urllib.parse import urlparse, urljoin
from app.extensions import mail 
from flask_mail import Message
from datetime import datetime
from app.extensions import *
from app.crypto import *
import re

user_datastore = None

def to_time(string): return datetime.strptime(string, "%H:%M").time() 

def to_date(string): return datetime.strptime(string, "%Y-%m-%d").date()

def send_email(subject, recipients, body_text=None, body_html=None):
    try:
        if not current_app.config.get('MAIL_SERVER'):
            raise RuntimeError("Erro: Flask-Mail não configurado no app.config!")
        
        for email in recipients:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError(f"Invalid email address: {email}")

        msg = Message(subject=subject, recipients=recipients)
        if body_html: msg.html = body_html
        if body_text: msg.html = body_text
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {e}")
        return False

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_user_datastore():
    return user_datastore

def create_roles():
    global user_datastore
    user_datastore.find_or_create_role(name='admin', description='Gerente do sistema')
    user_datastore.find_or_create_role(name='receptionist', description='Recepcionista do sistema')
    user_datastore.find_or_create_role(name='housekeeper', description='Camareira do sistema')
    user_datastore.find_or_create_role(name='guest', description='Hóspede do sistema')
    db.session.commit()

def create_app():
    from flask import Flask
    from flask_security import SQLAlchemyUserDatastore

    global user_datastore

    app = Flask(__name__)

    @app.template_filter()
    def currency(value, currency="BRL"):
        from babel.numbers import format_currency
        return format_currency(value, currency, locale="pt_BR")

    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    init_fernet(app)

    from app.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_blueprint=False)

    from app.routes import routes_bp, register_errors

    register_errors(app)
    app.register_blueprint(routes_bp, url_prefix='/')

    from app.seeds import seed_init
    seed_init(app)

    return app