from Question_Mark import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, session
from Question_Mark.models import User, Questions, Answers
from flask_login import login_user, current_user, logout_user, login_required
from random_username.generate import generate_username

@app.route("/register", methods=['GET','POST'])
def RegistrationForm():
    if current_user.is_authenticated:
        return redirect(url_for('explore'))
    if request.method == 'POST':
        first_name_ = request.form.get("f_name")
        last_name_ = request.form.get("l_name")
        a = generate_username(1)
        username_ = a[0]
        email_ = request.form.get("r_email")
        password_ = request.form.get("r_pass")
        confirm_password_ = request.form.get("c_pass")
        conditions = request.form.getlist('tc')
        hashed_password = bcrypt.generate_password_hash(password_).decode('utf-8')
        if password_ == confirm_password_:
            user = User(first_name=first_name_, last_name=last_name_, username=username_, email=email_, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You will now be able to log in!', 'success')
            return render_template('home.html', title='Home')
        else:
            flash('Account not created as password was not confirmed', 'info')
            return render_template('home.html', title='Home')
    return redirect(url_for('home'))
    
    

@app.route("/login", methods=['GET','POST'])
def LoginForm():
    if current_user.is_authenticated:
        return redirect(url_for('explore'))
    if request.method == 'POST':
        _email = request.form.get("l_email")
        _password = request.form.get("l_pass")
        _remember = request.form.getlist('checkbox')
        _user = User.query.filter_by(email=_email).first()
        if _user and bcrypt.check_password_hash(_user.password, _password):
            login_user(_user, remember=_remember)
            flash('Login Successful', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return render_template('home.html', title='Home')
    return redirect(url_for('home'))
    
        
@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('explore'))
    return render_template('home.html', title='Home')

    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/explore", methods=['GET','POST'])
def explore():
    values = Questions.query.order_by(Questions.date_posted.desc())
    if request.method == 'POST':
        _answer = request.form.get("answer")
        user = Answers( answer=_answer, quest_id=current_user.id )
        db.session.add(user)
        db.session.commit()
        flash('Your Answer has been posted successfully.', 'success')
        return redirect(url_for('explore'))
    return render_template('explore.html', title='Explore', values=values) 


@app.route("/faq")
def faq():
    return render_template('faq.html', title='FAQ')


@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    quest = Questions.query.filter_by(author=user)\
            .order_by(Questions.date_posted.desc())
    if request.method == 'POST':
        _question = request.form.get("question")
        user = Questions( question=_question, user_id=current_user.id )
        db.session.add(user)
        db.session.commit()
        flash('Your Question has been posted successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', title='Profile', user=user, quest=quest)


@app.route('/delete_ques/<string:id>', methods=['POST'])
def delete_ques(id):
    delete = Questions.query.filter_by(id=id).first()
    db.session.delete(delete)
    db.session.commit()
    flash("Question Deleted","success")
    return redirect(url_for('profile'))


@app.route("/user_posts/<username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    quest = Questions.query.filter_by(author=user)\
            .order_by(Questions.date_posted.desc())
    return render_template('user_posts.html', title='Profile: '+ username, x=username, user=user, quest=quest)
    

    
    
@app.route("/forgot_password", methods=['GET','POST'])
def forgot_password():
    return render_template('forgot_password.html', title='Forgot Password')





















