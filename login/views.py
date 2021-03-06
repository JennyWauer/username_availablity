from django.shortcuts import render, redirect

from .models import *

from django.contrib import messages

import bcrypt

def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if User.objects.filter(email=request.POST['email']):
            messages.error(request, 'Email is already registered. Please login!')
            return redirect('/')
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()    
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash
            )
            request.session['userid'] = new_user.id
            return redirect('/success')
    return redirect('/')

def user_login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['login_email'])
        if user:
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['login_pass'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/success')
        else:
            messages.error(request, 'Email/password combination not recognized. Please try again!')
        return redirect("/")

def log_off(request):
    if request.method == 'GET':
        return redirect('/books')
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')

def success(request):
    if 'userid' in request.session:
        user = User.objects.filter(id=request.session['userid'])
        if user:
            context = {
                "user": user[0]
            }
        return render(request, 'success.html', context)
    return redirect('/')

def email():
    found = False
    mysql = connectToMySQL('ajaxUsername_availability')        # connect to the database
    query = "SELECT email from users WHERE users.email = %(user)s;"
    data = { 'user': request.form['email'] }
    result = mysql.query_db(query, data)
    if result:
        found = True
    return render_template('partials/email.html', found=found)