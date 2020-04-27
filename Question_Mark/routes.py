from Question_Mark import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, session
from Question_Mark.models import User, Questions
from flask_login import current_user, logout_user, login_user

@app.route("/register", methods=['GET','POST'])
def RegistrationForm():
    if request.method == 'POST':
        first_name_ = request.form.get("f_name")
        last_name_ = request.form.get("l_name")
        email_ = request.form.get("r_email")
        password_ = request.form.get("r_pass")
        confirm_password_ = request.form.get("c_pass")
        conditions = request.form.getlist('tc')
        hashed_password = bcrypt.generate_password_hash(password_).decode('utf-8')
        user = User(first_name=first_name_, last_name=last_name_, email=email_, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You will now be able to log in!', 'success')
        return render_template('home.html', title='Home')
    else:
        return render_template('home.html', title='Home')
    

@app.route("/login", methods=['GET','POST'])
def LoginForm():
    if request.method == 'POST':
        _email = request.form.get("l_email")
        _password = request.form.get("l_pass" )
        _remember = request.form.getlist('checkbox')
        _user = User.query.filter_by(email=_email).first()
        if _user and bcrypt.check_password_hash(_user.password, _password):
            login_user(_user, remember=_remember)
            flash('Login Successful', 'success')
            return render_template('profile.html', title='Profile')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('home.html', title='Home')
    
    


@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    RegistrationForm()
    return render_template('home.html', title='Home')
            
        

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/explore")
def explore():
    return render_template('explore.html', title='Explore')


@app.route("/faq")
def faq():
    return render_template('faq.html', title='FAQ')
























