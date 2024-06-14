from ledger import app,mongo
from ledger.forms import *
from flask import render_template,request,flash,session,redirect,url_for

@app.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        print(mongo.db)
        user = mongo.db.users.find_one({'username':form.username.data, 'password':form.password.data})
        if user:
            flash("Logged in successfully")
            session['user'] = form.username.data
            session.permanent=True
            return redirect(url_for('dashboard'))
        flash("Invalid credentials")
    return render_template('login.html',form=form) 

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if "user" in session:
        name = session['user']
        customers = mongo.db.customers.find({}).sort({'name':1})
        return render_template('dashboard.html',name=name,customers=customers)
    return redirect(url_for('login')) 

@app.route('/add_customer',methods=['GET','POST'])
def add():
    if "user" in session:
        form = AddCustomerForm()
        if request.method=='POST':
            mongo.db.customers.insert_one({
                'phone':form.phone.data,
                'name':form.name.data,
                'address':form.address.data,
                'balance':form.balance.data
            })
            flash("Customer added successfully")
            return redirect(url_for('dashboard'))
        return render_template('add_customer.html',form=form)
    return redirect(url_for('login')) 

@app.route('/logout')
def logout():
    session.pop('user',None)  
    flash("Logged out successfully")
    return redirect(url_for('login')) 

@app.route('/posts/sort/<string:sort_selected>')
def sort(sort_selected):
    if "user" in session:
        if sort_selected=='week':
            minus_days=-7
            sorted_by='Past Week'
        elif sort_selected=='month':
            minus_days=-30
            sorted_by='Past Month'
        elif sort_selected=='year':
            minus_days=-365
            sorted_by='Past Year'
        else:
            return render_template('404.html'), 404
        posts=mongo.db.customers.find().sort({'name':1})
        return render_template('posts.html',posts=posts,sorted_by=sorted_by) 
    return redirect(url_for('login'))