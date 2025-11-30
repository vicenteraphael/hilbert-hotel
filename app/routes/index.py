from flask import render_template, redirect, url_for
from app.routes import routes_bp
from flask_login import current_user, login_required
from flask_security import roles_accepted
from app.models import User
from app import db

@routes_bp.route('/')
def index():
    if 'admin' in current_user.roles: return redirect(url_for('routes.admin'))
    if 'receptionist' in current_user.roles: return redirect(url_for('routes.receptionist'))
    if 'housekeeper' in current_user.roles: return redirect(url_for('routes.housekeeper'))
    if 'guest' in current_user.roles: return redirect(url_for('routes.guest'))
    return render_template('index.html')

@routes_bp.route('/admin')
@login_required
@roles_accepted('admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

@routes_bp.route('/receptionist')
@login_required
@roles_accepted('receptionist')
def receptionist():
    return render_template('reception.html')

@routes_bp.route('/housekeeper')
@login_required
@roles_accepted('housekeeper')
def housekeeper():
    return render_template('housekeeping.html')