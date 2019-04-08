from flask import Flask, render_template, request, session, flash, redirect, url_for
from DatabaseHelper import dataBase
from DoctorsData import jsonData
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



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login(title=""):
    return  render_template('login.html',error = title)

@app.route('/log',methods=['POST'])
def do_admin_login():
        flag = valid_user(request)
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
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('logged_in')
    return redirect(url_for('home'))

@app.route('/dentist')
def dentist():
    data = jsonData()
    list = data['dentist']
    return render_template('card.html',doctors=list)


@app.route('/ENT')
def ENT():
    data = jsonData()
    list = data['ent']
    return render_template('card.html', doctors=list)


@app.route('/dermatologist')
def dermatologist():
    data = jsonData()
    list = data['dermo']
    return render_template('card.html', doctors=list)


@app.route('/neurologist')
def neurologist():
    data = jsonData()
    list = data['neuro']
    return render_template('card.html', doctors=list)


@app.route('/podiatrist')
def podiatrist():
    data = jsonData()
    list = data['pod']
    return render_template('card.html', doctors=list)


@app.route('/physicalTherapist')
def physicalTherapist():
    data = jsonData()
    list = data['phy']
    return render_template('card.html', doctors=list)


if __name__ == '__main__':
    app.run(debug=True)