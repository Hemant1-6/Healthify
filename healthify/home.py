from flask import Flask, render_template, request, session, flash, redirect, url_for
from DatabaseHelper import dataBase
from DoctorsData import jsonData
from blog_data import blog_data

appt = []

app = Flask(__name__)
app.secret_key = "Healthify"

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
       str = """select count(*),name from usrInfo where password = %s and email = %s """
       cursor.execute(str,(req.form['password'],req.form['email'],))
       a = cursor.fetchone()
    return a

#booking appointment data
def appoint_data(req: 'Appointment',doc: 'doctor',fee: 'fee') -> None:
    with dataBase(app.config['dbconfig']) as cursor:
        str = """insert into appoint(doc_name,patient_name,time,phn_number,fee) values (%s,%s,%s,%s,%s) """
        cursor.execute(str, (doc,session['name'], req.form['time'], req.form['contact'],fee, ))


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
        session['name'] = flag[1]
        if flag[0]:
            session['logged_in'] = True
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
        return render_template('booking.html',doctor=data[0],patient=session['name'],time=data[1],fee=data[2])


@app.route('/appointment',methods=['POST'])
def appoint():
    global appt
    appoint_data(request,appt[0],appt[1])
    return home()


@app.route('/<string:page_name>/')
def rend(page_name):
  return render_template('%s.html' % page_name)

if __name__ == '__main__':
    app.run(debug=True)