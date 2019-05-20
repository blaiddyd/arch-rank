from flask import render_template, jsonify
from app import app, db
from app.forms import Login, SignUp, CitizenReport, CitizenStatus, Eval
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
            print('There was an error creating new user.' + str(e))
    return render_template(
        'register.html', links=get_links(), title='Join Arch', form=form)


@app.route('/evaluation', methods=['GET', 'POST'])
@login_required
def eval():
    form = Eval()
    if form.validate_on_submit():
        citizen = Citizen.query.filter_by(
            citizen_id=current_user.citizen_id).first_or_404()
        citizen.name = form.full_name.data
        print(form.full_name.data)
        db.session.commit()
    print('nope')
    return render_template(
        'eval.html',
        links=get_links(),
        title='Evaluation',
        form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form = Login()
    if not form.validate_on_submit():
        print('Form did not validate')
    if form.validate_on_submit():
        citizen = Citizen.query.filter_by(
            citizen_id=form.citizen_id.data).first()
        if citizen is None or not citizen.check_password(form.password.data):
            flash('Incorrect Citizen ID or Password')
            return redirect(url_for('login'))
        login_user(citizen)
        return redirect(url_for('feed'))
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
            return redirect(url_for('feed'))
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
        reports_page, 5, False)
    next_reports = url_for('feed', reports=reports.next_num) \
        if reports.has_next else None
    prev_reports = url_for('feed', reports=reports.prev_num) \
        if reports.has_prev else None
    all_status = Status.query.order_by(
        Status.timestamp.desc()).paginate(
        status_page, 5, False)
    next_statuses = url_for('feed', status=all_status.next_num) \
        if all_status.has_next else None
    prev_statuses = url_for('feed', status=all_status.prev_num) \
        if all_status.prev else None
    return render_template(
        'feed.html',
        title='Feed',
        form=form,
        reports=reports.items,
        status_input=status_input,
        statuses=all_status.items,
        next_reports=next_reports,
        prev_reports=prev_reports,
        next_status=next_statuses,
        prev_status=prev_statuses)


@app.route('/profile')
@login_required
def profile_home():
    user_id = current_user.citizen_id
    return redirect(url_for('profile', citizen_id=user_id))


@app.route('/profile/<citizen_id>')
@login_required
def profile(citizen_id):
    citizen = Citizen.query.filter_by(citizen_id=citizen_id).first_or_404()
    title = citizen.name
    is_self = False
    if citizen_id == current_user.citizen_id:
        is_self = True
        title = 'My Profile'
    return render_template(
        'profile.html', title=title, citizen=citizen, is_self=is_self)


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
    client_id = app.config['IMG_ACCESS']
    orientation = 'squarish'
    count = nums
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
        Citizen.score >= 5000).order_by(
        func.random()).limit(3)
    return render_template(
        'rank.html',
        citizens=citizens.items,
        tops=top_citizens,
        next=next_citizens,
        prev=prev_citizens,
        title="Rank")
