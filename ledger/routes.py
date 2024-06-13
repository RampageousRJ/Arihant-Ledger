from ledger import app
from ledger.forms import LoginForm
from flask import render_template

@app.route('/')
def login():
    form = LoginForm()
    return render_template('login.html',form=form)