from flask import render_template, jsonify
from app import app, db
from app.forms import Login, SignUp, CitizenReport, CitizenStatus, DeleteUser, Eval  # nopep8
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Citizen, Report, Status, Image
from flask import redirect, url_for, flash, request
from sqlalchemy import func
import string
import random
from requests import get


def gen_id():
    chars = string.digits
    return int(''.join(random.choice(chars) for _ in range(0, 6)))


def get_links():
    return [
        {
            'text': 'About',
            'path': url_for('about')
        },
        {
            'text': 'Rank',
            'path': url_for('rank')
        },
        {
            'text': 'Login',
            'path': url_for('login')
        }
    ]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome', links=get_links())


@app.route('/about')
def about():
    return 'This is about'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = SignUp()
    if form.validate_on_submit():
        try:
            citizen = Citizen(
                citizen_id=form.citizen_id.data,
                name=form.citizen_id.data,
                score=20000,
                profile_image=url_for(
                    'static', filename='assets/blank_profile.png'
                )
            )
            citizen.set_password(form.password.data)
            db.session.add(citizen)
            db.session.commit()
            login_user(citizen)
            return redirect(url_for('feed'))
        except Exception as e:
            flash('User already exists')
            print('There was an error creating new user.' + str(e))
    return render_template(
        'register.html', links=get_links(), title='Join Arch', form=form)


def gen_score(form):
        score = 30000
        score += (3 - int(form.island.data[0])) * 2500
        score += (4 - int(form.profession.data[0])) * 3000
        score += (form.income.data/100)
        score += int(form.kids.data[0])*500
        score += int(form.lonely.data) * -1000
        return score


@app.route('/evaluation', methods=['GET', 'POST'])
@login_required
def eval():
    citizen = Citizen.query.filter_by(
            citizen_id=current_user.citizen_id).first()
    if citizen.eval_complete:
        return redirect(url_for('feed'))
    form = Eval()
    print(form.birth_date.data)
    if form.validate_on_submit():
        citizen = Citizen.query.filter_by(
            citizen_id=current_user.citizen_id).first()
        citizen.name = form.full_name.data
        citizen.score = gen_score(form)
        citizen.eval_complete = 1
        random_img = random.choice(Image.query.all()).image_url
        citizen.set_pic(random_img)
        db.session.commit()
        return redirect('feed')
    else:
        print('Form did not validate ' + str(form.errors))
    return render_template(
        'eval.html',
        title='Evaluation',
        form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = Login()
    if not form.validate_on_submit():
        print('Form did not validate ')
    if form.validate_on_submit():
        citizen = Citizen.query.filter_by(
            citizen_id=form.citizen_id.data).first()
        if citizen is None or not citizen.check_password(form.password.data):
            flash('Incorrect Citizen ID or Password')
            return redirect(url_for('login'))
        login_user(citizen)
        if citizen.permission != 'admin':
            return redirect(url_for('feed'))
        else:
            return redirect(url_for('admin_board'))
    return render_template(
        'login.html',
        form=form,
        links=get_links(),
        title="Login")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    citizen = Citizen.query.filter_by(
            citizen_id=current_user.citizen_id).first()
    if not citizen.eval_complete:
        return redirect(url_for('eval'))
    invalid_citizen = False
    submit_error = False
    status_page = request.args.get('status', 1, type=int)
    reports_page = request.args.get('reports', 1, type=int)
    form = CitizenReport(reporter=current_user.citizen_id)
    status_input = CitizenStatus()
    if form.validate_on_submit():
        reported = Citizen.query.filter_by(
            citizen_id=form.traitor.data).first()
        if reported is None:
            invalid_citizen = True
        else:
            try:
                reported.score = reported.score + float(form.category.data)
                db.session.commit()
                subject = value = dict(
                    form.category.choices).get(
                    form.category.data)
                new_report = Report(
                    reporter_id=current_user.citizen_id,
                    reported_id=reported.citizen_id,
                    report_id=gen_id(),
                    report_category=subject,
                    body=form.body.data)
                db.session.add(new_report)
                db.session.commit()
                print('Successful report submission')
            except Exception as score_error:
                print('Report submission error: ' + str(score_error))
    else:
        print('Report form validation error')
        print(form.errors)
    if status_input.validate_on_submit():
        try:
            current_citizen = Citizen.query.filter_by(
                citizen_id=current_user.citizen_id).first()
            if current_citizen is None:
                invalid_citizen = True
            else:
                current_citizen.score = current_citizen.score + \
                    float(status_input.status_category.data)
                db.session.commit()
                status_subject = dict(
                    status_input.status_category.choices).get(
                    status_input.status_category.data)
                new_status = Status(
                    citizen_id=current_user.citizen_id,
                    status_id=gen_id(),
                    status_category=status_subject,
                    body=status_input.status.data)
                db.session.add(new_status)
                db.session.commit()
                print('Status submission successful')
        except Exception as status_error:
            print('Status submission error: ' + str(status_error))
    else:
        print('Status form validation error')
        print(status_input.errors)
    reports = Report.query.order_by(
        Report.time.desc()).paginate(
        reports_page, 20, False)
    all_status = Status.query.order_by(
        Status.timestamp.desc()).paginate(
        status_page, 20, False)
    return render_template(
        'feed.html',
        title='Feed',
        form=form,
        reports=reports.items,
        status_input=status_input,
        statuses=all_status.items,
        invalid_citizen=invalid_citizen
    )


@app.route('/profile')
@login_required
def profile_home():
    citizen = Citizen.query.filter_by(
            citizen_id=current_user.citizen_id).first()
    if not citizen.eval_complete:
        return redirect(url_for('eval'))
    user_id = citizen.citizen_id
    return redirect(url_for('profile', citizen_id=user_id))


@app.route('/profile/<citizen_id>')
@login_required
def profile(citizen_id):
    status_page = request.args.get('page', 1, type=int)
    citizen = Citizen.query.filter_by(citizen_id=citizen_id).first_or_404()
    title = citizen.name
    is_self = False
    all_status = Status.query.filter_by(citizen_id=citizen.citizen_id).order_by(
        Status.timestamp.desc()).paginate(
        status_page, 20, False)
    next = url_for('profile', citizen_id=citizen.citizen_id, status_page=all_status.next_num) \
        if all_status.has_next else None
    prev = url_for('profile', citizen_id=citizen.citizen_id, status_page=all_status.prev_num) \
        if all_status.has_prev else None
    if citizen_id == current_user.citizen_id:
        is_self = True
        title = 'My Profile'
    return render_template(
        'profile.html', title=title, citizen=citizen, is_self=is_self, status=all_status.items, next=next, prev=prev)


@app.route('/profile/random_img')
@login_required
def random_profile():
    citizen = Citizen.query.filter_by(
        citizen_id=current_user.citizen_id).first_or_404()
    random_img = random.choice(Image.query.all()).image_url
    citizen.set_pic(random_img)
    db.session.commit()
    return redirect(url_for('profile', citizen_id=current_user.citizen_id))


def get_images(num):
    print("Getting images")
    client_id = app.config['IMG_ACCESS']
    orientation = 'squarish'
    count = num
    url = 'https://api.unsplash.com/photos/random/?client_id={}&orientation={}&count={}'.format(client_id, orientation, count)  # nopep8
    content = get(url).json()
    for img in content:
        image = Image(image_url=img['urls']['small'])
        db.session.add(image)
    db.session.commit()


@app.route('/rank')
def rank():
    page = request.args.get('page', 1, type=int)
    citizens = Citizen.query.order_by(
        Citizen.score.desc()).paginate(
        page, 10, False)
    next_citizens = url_for('rank', page=citizens.next_num) \
        if citizens.has_next else None
    prev_citizens = url_for('rank', page=citizens.prev_num) \
        if citizens.has_prev else None
    top_citizens = Citizen.query.filter(
        Citizen.score >= 60000).order_by(
        func.random()).limit(3)
    return render_template(
        'rank.html',
        citizens=citizens.items,
        tops=top_citizens,
        next=next_citizens,
        prev=prev_citizens,
        title="Rank")


@app.route('/admin_board', methods=['GET', 'POST'])
@login_required
def admin_board():
    success = False
    error = False
    if str(current_user.permission) != 'admin':
        return redirect(url_for('feed'))
    else:
        delete_user = DeleteUser()
        page = request.args.get('page', 1, type=int)
        citizens = Citizen.query.order_by(
            Citizen.score.desc()).paginate(
            page, 10, False)
        next_citizens = url_for('page', page=citizens.next_num) \
            if citizens.has_next else None
        prev_citizens = url_for('page', page=citizens.prev_num) \
            if citizens.has_prev else None
        if delete_user.validate_on_submit():
            try:
                delete_citizen = Citizen.query.filter_by(
                    citizen_id=delete_user.citizen_id.data).first()
                if delete_citizen is None:
                    error = True
                else:
                    delete_citizen.delete()
                    db.session.commit()
                    print('Deleted user.')
                    success = True
            except Exception as e:
                print('Error in deleting user ' + str(e))
                error = True
        else:
            print('Form did not validate')
            print(str(delete_user.errors))
        return render_template(
            'admin.html',
            title="Webmaster Dashboard",
            citizens=citizens.items,
            success=success,
            error=error,
            delete=delete_user,
            next=next_citizens,
            prev=prev_citizens)
