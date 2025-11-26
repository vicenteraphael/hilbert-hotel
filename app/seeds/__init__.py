from app.seeds.generate_users import seed_users
import subprocess

def seed_all(app):
    @app.cli.command("seed_all")
    def seed():
        with app.app_context():
            print("Iniciando o seeding de todos os dados...")
            subprocess.run(["flask", "seed_users"], check=True)

def seed_init(app):
    seed_users(app)
    seed_all(app)