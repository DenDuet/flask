from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

from forms import RegistrationForm
from models import db, User

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'

csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///users.db'
db.init_app(app)


@app.route('/init_db/', methods=['GET', 'POST'])
def init_db():
    db.create_all()
    print("ОК")


@app.route('/')
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        hash = generate_password_hash(request.form['password'])
        existing_user = User.query.filter(
            (User.username == username) & (
                User.lastname == lastname) | (User.email == email)
        ).first()
        if existing_user:
            error_msg = 'Username or email already exists.'
            form.username.errors.append(error_msg)
            return render_template('register.html', form=form)
        new_user = User(username=username, lastname=lastname,
                        email=email, password=hash)
        db.session.add(new_user)
        db.session.commit()

        # Выводим сообщение об успешной регистрации
        success_msg = 'Registration successful!'
        return success_msg

    return render_template('register.html', form=form)


@app.route("/users/")
def table():
    users = User.query.all()
    # .filter_by(faculty_id=id)
    context = {'users': users}
    for user in users:
        print(f'context = {user}')
    return render_template('users.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
