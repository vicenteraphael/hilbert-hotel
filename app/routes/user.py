from flask import render_template, request, jsonify, url_for, redirect
from flask_security import roles_accepted
from flask_login import login_required, current_user
from app.routes import routes_bp
from app.models import User, select_users_with_role
from app import db, get_user_datastore, login_manager

# USER PORTAL

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@routes_bp.route('/user')
@login_required
def user():
    return redirect(url_for('main.UserData', UserData_chosen='1'))

@routes_bp.route('/user/2/api/cancel', methods=['POST'])
@login_required
def cancel_rent():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()

        #insert logic
        if data:
            return jsonify({
                "success" : True,
                "title" : "Locação cancelada com sucesso",
                "icon" : "success"
            })
        
        return jsonify({
                "success" : False,
                "title" : "Locação não encontrada",
                "icon" : "error"
            })

# DASHBOARD

@routes_bp.route('/dashboard/clients')
@login_required
@roles_accepted('manager', 'worker')
def list_clients():
    clients = select_users_with_role('client')
    if 'manager' in current_user.roles:
        user_role = 'manager'
    else:
        user_role = 'worker'
    return render_template('main/listperson.html', user_role=user_role, list='clientes', list_role='client', users=clients)
    
@routes_bp.route('/dashboard/workers')
@login_required
@roles_accepted('manager')
def list_workers():
    workers = select_users_with_role('worker')
    if 'manager' in current_user.roles:
        user_role = 'manager'
    else:
        user_role = 'worker'
    return render_template('main/listperson.html', user_role=user_role, list='funcionários', list_role='worker', users=workers)

@routes_bp.route('/dashboard/managers')
@login_required
@roles_accepted('manager')
def list_managers():
    if 'manager' in current_user.roles:
        user_role = 'manager'
    else:
        user_role = 'worker'
    managers = select_users_with_role('manager')
    return render_template('main/listperson.html', user_role=user_role, list='gerentes', list_role='manager', users=managers)


@routes_bp.route('dashboard/controll')
@login_required
@roles_accepted('manager', 'worker')
def dashboard_controll():
    return render_template('main/dashboardControll.html', user_name=current_user.name)

@routes_bp.route('/dashboard/api/promote', methods=['POST'])
@login_required
@roles_accepted('worker', 'manager')
def promote_user():
    if request.method == "POST" and request.is_json:
        data = request.get_json()

        user_id = int(data.get("id"))
        user_role = data.get("role")
        promotion = data.get("promotion")

        user = User.query.get(int(user_id))
        if user:
            user_datastore = get_user_datastore()
            user_datastore.remove_role_from_user(user, user_role)
            user_datastore.add_role_to_user(user, promotion)

            db.session.commit()

            return jsonify({
                "success" : True,
                "title" : "Usuário promovido com sucesso",
                "icon" : "success"
            })

        return jsonify({
            "success" : False,
            "title" : "Usuário não cadastrado",
            "icon" : "error"
        })
