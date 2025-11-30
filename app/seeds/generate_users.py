from app import get_user_datastore, bcrypt, db, faker
from random import randint
import hashlib

def seed_users(app):

    @app.cli.command("seed_users")
    def seed(qnt_users=12):

        user_datastore = get_user_datastore()
        #creates n fake users
        roles = (qnt_users//3)*(['receptionist']+['guest']+['housekeeper'])
        while len(roles) != qnt_users: roles.append('housekeeper')
        for _ in range (qnt_users):
            name = faker.first_name()
            first_name = name.lower().split()[0]
            email = f"{first_name}{randint(100, 999)}@test.com"
            hashed_email = hashlib.sha256(email.encode()).hexdigest()
            cpf = faker.cpf()
            if not user_datastore.find_user(email_hash=hashed_email):
                hashed_password = bcrypt.generate_password_hash(f"{first_name}{12345}").decode('utf-8')
                user = user_datastore.create_user(
                    name=name,
                    email=email,
                    password=hashed_password,
                    cpf=cpf
                )
                user_datastore.add_role_to_user(user, roles.pop())
            print(user)
                

        #create the manager
        email = "admin@test.com"
        hashed_email = hashlib.sha256(email.encode()).hexdigest()
        if not user_datastore.find_user(email_hash=hashed_email):
            admin = user_datastore.create_user(
                name = "Raphael Vicente",
                email = email,
                password = bcrypt.generate_password_hash("abc12345").decode('utf-8'),
                cpf = "08189671068"
            )
            user_datastore.add_role_to_user(admin, "admin")
            print("Create admin:", admin)

        #create a receptionist
        email = "receptionist@test.com"
        hashed_email = hashlib.sha256(email.encode()).hexdigest()
        if not user_datastore.find_user(email_hash=hashed_email):
            receptionist = user_datastore.create_user(
                name = "Ricardo Agostinho",
                email = email,
                password = bcrypt.generate_password_hash("abc12345").decode('utf-8'),
                cpf = "08149370068"
            )
            user_datastore.add_role_to_user(receptionist, "receptionist")
            print("Create receptionist:", receptionist)

        email = "housekeeper@test.com"
        hashed_email = hashlib.sha256(email.encode()).hexdigest()
        if not user_datastore.find_user(email_hash=hashed_email):
            housekeeper = user_datastore.create_user(
                name = "Letícia Martins",
                email = email,
                password = bcrypt.generate_password_hash("abc12345").decode('utf-8'),
                cpf = "98299673467"
            )
            user_datastore.add_role_to_user(housekeeper, "housekeeper")
            print("Create admin:", housekeeper)

        db.session.commit()