from flask import Blueprint

routes_bp = Blueprint('routes', __name__, template_folder='templates')

from app.routes import errors, index, login, register, user, worker
from app.routes.errors import register_errors