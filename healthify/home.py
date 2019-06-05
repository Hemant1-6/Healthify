from flask import Flask, render_template, request, session, flash, redirect, url_for
from DatabaseHelper import dataBase
from DoctorsData import jsonData
import sqlite3

appt = []

app = Flask(__name__)
app.secret_key = "Healthify"
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# database configurations
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'healthify',
                          'password': 'health',
                          'database': 'logindb', }


#register user into database
def log_user(req: 'Register') -> None:
    with dataBase(app.config['dbconfig']) as cursor:
        str = """insert into usrInfo(name,email,sex,state,city,address,password) values (%s,%s,%s,%s,%s,%s,%s) """
        cursor.execute(str, (req.form['name'], req.form['email'], req.form['sex'], req.form['state'], req.form['city'], req.form['address'], req.form['password'], ))


#validate user credentials
def valid_user(req:'login')->int:
    with dataBase(app.config['dbconfig']) as cursor:
       str = """select count(*),name,email,userId from usrInfo where password = %s and email = %s """
       cursor.execute(str,(req.form['password'],req.form['email'],))
       a = cursor.fetchone()
    return a

#booking appointment data
def appoint_data(req: 'Appointment',doc: 'doctor',fee: 'fee') -> None:
    with dataBase(app.config['dbconfig']) as cursor:
        str = """insert into appoint(doc_name,patient_name,time,phn_number,fee) values (%s,%s,%s,%s,%s) """
        cursor.execute(str, (doc,session['name'], req.form['time'], req.form['contact'],fee, ))


def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            userId = session['userId']
            firstName = session['name']
            cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)


@app.route('/')
def home():
   if 'logged_in' not in session:
    return render_template('home.html')
   else:
       return render_template('logout.html')


@app.route('/login')
def login(title=""):
    return  render_template('login.html',error = title)

@app.route('/log',methods=['POST'])
def do_admin_login():
        flag = valid_user(request)
        if flag[0]:
            session['logged_in'] = True
            session['name'] = flag[1]
            session['email'] = flag[2]
            session['userId'] = flag[3]
            return render_template('logout.html')
        else:
            return login(title="wrong username or password!")

@app.route('/register')
def do_register():
 if not session.get('logged_in'):
    return render_template('register.html')
 else :
     return render_template('home.html')

@app.route('/info',methods=['POST'])
def user_info():
    log_user(request)
    # rqst_name(request)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('logged_in')
    return redirect(url_for('home'))

@app.route('/dentist')
def dentist():
    data = jsonData()
    list = data['dentist']
    session['doclist'] = list
    return render_template('card.html',doctors=list)


@app.route('/ENT')
def ENT():
    data = jsonData()
    list = data['ent']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/dermatologist')
def dermatologist():
    data = jsonData()
    list = data['dermo']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/neurologist')
def neurologist():
    data = jsonData()
    list = data['neuro']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/podiatrist')
def podiatrist():
    data = jsonData()
    list = data['pod']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/physicalTherapist')
def physicalTherapist():
    data = jsonData()
    list = data['phy']
    session['doclist'] = list
    return render_template('card.html', doctors=list)


@app.route('/spn',methods=['GET'])
def spn():
    doc = []
    value = request.args["city"]
    list = session['doclist']
    for ls in list:
        if ls['address']['city'] == value:
            doc.append(ls)
    return render_template('card.html',doctors=doc)

@app.route('/book',methods=['GET'])
def book():
    if 'logged_in' not in session:
        return login(title="Please login First")
    else:
        value = request.args['submit']
        data = value.split(',')
        global appt
        appt.append(data[0])
        appt.append(data[2])
        print(appt)
        return render_template('booking.html',doctor=data[0],patient=session['name'],time=data[1],fee=data[2])


@app.route('/appointment',methods=['POST'])
def appoint():
    global appt
    appoint_data(request,appt[0],appt[1])
    appt.clear()
    return home()


@app.route('/ordermedicine')
def order():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products')
        itemData = cur.fetchall()
    itemData = parse(itemData)
    print(itemData)
    return render_template('order.html', itemData=itemData, loggedIn=loggedIn  , noOfItems=noOfItems,)

@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ?', (productId, ))
        productData = cur.fetchone()
    conn.close()
    return render_template("productDescription.html", data=productData, loggedIn = loggedIn, noOfItems = noOfItems)

@app.route("/addToCart")
def addToCart():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            userId = session['userId']
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('order'))

@app.route("/ordercart")
def cart():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        userId = session['userId']
        cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ?", (userId, ))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/removeFromCart",methods=['GET'])
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    productId = int(request.args.get('remove'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        userId = session['userId']
        try:
            cur.execute("DELETE FROM kart WHERE userId = ? AND productId = ?", (userId, productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('order'))



@app.route('/<string:page_name>/')
def rend(page_name):
  return render_template('%s.html' % page_name)

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)