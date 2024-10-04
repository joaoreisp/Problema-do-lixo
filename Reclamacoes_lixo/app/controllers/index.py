from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from run import app

@app.route('/')
def indexuser():
   try:
        return render_template('index.html')
   except Exception as e:
        print(e)
        return render_template('error.html')