import os.path
from flask import render_template, flash, redirect, session, url_for, request, g, Flask, Response
from flask.ext.login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin 
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.file import FileField
from app import app, db, login_manager
from .forms import *
from .emails import *
from .models import User, PortfolioItem
from datetime import datetime

import markdown


@login_manager.user_loader
def user_loader(user_id):
    
    return User.query.filter_by(email=user_id).first()

@app.before_request
def before_request():
    g.user = current_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    name = ''
    contactform = ContactForm()
    form_submitted=False
    if contactform.validate_on_submit():
        name=contactform.name.data
        email=contactform.email.data
        subject=contactform.subject.data
        message=contactform.message.data
        form_submitted=True
          
        html = render_template('email.html', name=name, subject=subject, message=message)
        
        email_name = name + "<" + email + ">"
        
        email_result = send_email(email_name, subject, message, html)
                           
    form = PortfolioItemForm()
    if form.validate_on_submit():
        description = form.description.data
        filename = form.artwork_path.data.filename
        pfi = PortfolioItem(description=description,
                    name=form.name.data,
                    artwork_path=filename)
        form.artwork_path.data.save('./app/static/img/artwork/' + filename)
        db.session.add(pfi)
        db.session.commit()
        return redirect(url_for('index'))

    items = PortfolioItem.query.all()
    return render_template('index.html',
                           title='Portfolio',
                           form=form,
                           items=items,
                           contactform=contactform,
                           form_submitted=form_submitted,
                           name=name)

def contact():
    name = ''
    contactform = ContactForm()
    form_submitted=False
    if contactform.validate_on_submit():
        name=contactform.name.data
        email=contactform.email.data
        subject=contactform.subject.data
        message=contactform.message.data
        form_submitted=True
          
        html = render_template('email.html', name=name, subject=subject, message=message)
        
        email_name = name + "<" + email + ">"
        
        email_result = send_email(email_name, subject, message, html)
        
    return render_template('index.html',
                           title='Contact',
                           contactform=contactform,
                           form_submitted=form_submitted,
                           name=name)

@app.route('/index/<int:id>', methods=['GET'])
def view_artwork(id):
    item = PortfolioItem.query.get(id)
    return render_template('artwork_container.html',
                           title='Portfolio',
                           item=item)
                           
@app.route('/delete_portfolioitem/<int:id>')
def delete_portfolioitem(id):
    item = PortfolioItem.query.get(id)
    if item is None:
        flash('Artwork not found.')
        return redirect(url_for('index'))
    db.session.delete(item)
    db.session.commit()
    flash('Your Artwork has been deleted.')
    return redirect(url_for('index'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    #if g.user is not None and g.user.is_authenticated:
    #    return redirect(url_for('index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        if form.nickname.data is None or form.nickname.data == "":
            flash('Invalid login. Please try again.')
            return redirect(url_for('login'))
            
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if user is None:
            flash('username not found.')
            return redirect(url_for('login'))
        if user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for("index"))
        flash('password not found.')
        return redirect(url_for('login'))
    return render_template("login.html", form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    