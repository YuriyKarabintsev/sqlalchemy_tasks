import flask
from flask import Flask
from flask import render_template
from loginform import LoginForm
from jobsform import JobsForm
from userform import UserForm
from data.users import User
from data import db_session
from flask_login import login_user
from flask import redirect
from flask_login import LoginManager
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/")
def index():
    print("index")
    return render_template('base.html', title='Заготовка')

@app.route("/training/<prof>")
def profession(prof):
    print(prof)
    return render_template("prof.html", prof=prof)

@app.route("/list_prof/<list_type>")
def show_list(list_type):
    professions = ["инженер-исследователь", "пилот", "строитель", "экзобиолог", "врач",
                   "инженер по терраформированию", "климатолог", "специалист по радиационной защите",
                   "астрогеолог", "гляциолог", "инженер жизнеобеспечения", "метеоролог",
                   "оператор марсохода", "киберинженер", "штурман", "пилот дронов"]
    return render_template("show_list.html", list_type=list_type, professions=professions)

@app.route("/answer")
@app.route("/auto_answer")
def answer():
    inf = {
        "title": "Анкета",
        "name": "Mark",
        "surname": "Watny",
        "education": "выше среднего",
        "profession": "штурман марсохода",
        "sex": "male",
        "motivation": "Всегда мечтал застрять на Марсе!",
        "ready": True
    }
    return render_template("auto_answer.html", inf=inf, title=inf["title"])


@app.route('/login', methods=['GET', 'POST'])
def login():
    registration = False

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data) and User.login == form.login.data: # атрибуты для задачи
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, registration=registration)

@app.route("/registration", methods=["GET","POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.id = form.id.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.hashed_password = form.hashed_password.data
        user.modified_date = form.modified_date.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template("registration.html", form=form)

@app.route('/addjob', methods=['GET', 'POST'])
def jobs_add():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        db_sess.add(jobs)
        db_sess.commit()
        for user in db_sess.query(User).all():
            print(user.id, user.name, user.surname, "User")


        return redirect('/')
    return render_template("form_add.html", form=form, message="Submit", title="Adding a job")


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")

print("works")