from ledger import app,mongo
from ledger.forms import *
from flask import render_template,request,flash,session,redirect,url_for
from datetime import datetime

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

@app.route('/new-order/',methods=['GET','POST'])
def new_order():
    if "user" in session:
        form = OrderForm()
        if request.method=='POST':
            phone = form.phone.data
            customer = mongo.db.customers.find_one({'phone':phone})
            if not customer:
                flash("Customer not found")
                return redirect(url_for('new_order'))
            mongo.db.orders.insert_one({
                'phone':form.phone.data,
                'detail':form.detail.data,
                'amount':form.amount.data,
                'paid':form.paid.data,
                'date_added':datetime.now()
            })
            try:
                mongo.db.customers.update_one({ "phone": form.phone.data}, { "$set": { "balance": customer['balance'] - form.amount.data + form.paid.data}})
            except Exception as e:
                print(e)
                flash("Error updating balance")
            flash("Order added successfully")
            return redirect(url_for('new_order'))
        return render_template('orders.html',form=form)
    return redirect(url_for('login'))

@app.route('/history/')
def history():
    if "user" in session:
        orders = mongo.db.orders.aggregate([{
                                            "$lookup": {
                                            "from": "customers",
                                            "localField": "phone", 
                                            "foreignField": "phone",
                                            "as": "customer"
                                            }
                                        },
                                        {
                                            "$unwind": "$customer"
                                        },
                                        {
                                            "$project": {
                                            "order_id": "$_id",
                                            "phone": 1,
                                            "detail": 1,
                                            "amount": 1,
                                            "paid": 1,
                                            "date_added": 1,
                                            "customer.phone": 1, 
                                            "customer.name": 1,
                                            "customer.address": 1,
                                            "customer.balance": 1
                                            }
                                        },
                                        {
                                            "$sort": {"date_added": -1} 
                                        }
                                    ])
        return render_template('history.html',orders=orders)
    return redirect(url_for('login'))

@app.route('/customer/<string:phone>')
def customer(phone):
    if "user" in session:
        customer = mongo.db.customers.find_one({'phone':phone})
        orders = mongo.db.orders.find({'phone':phone}).sort({'date_added':-1})
        return render_template('customer.html',customer=customer,orders=orders)
    return redirect(url_for('login'))