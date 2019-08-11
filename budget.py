from app import create_app, db
from app.models import Category, LineItem, User


app = create_app()
with app.app_context():

    username = app.config['ADMIN_USERNAME']
    admin = User.query.filter_by(username=username).first()
    email = app.config['ADMIN_EMAIL']
    password = app.config['ADMIN_PASSWORD']
    if admin is None:
        if not email:
            email = 'admin@admin.adm'
        admin = User(username='admin', email=email)
        if not password:
            password = 'admin1234'
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
    else:
        if password:
            admin.set_password(password)
            db.session.commit()

    if not admin.active:
        admin.active = True
        db.session.commit()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Category': Category, 'LineItem': LineItem, 'User': User}
