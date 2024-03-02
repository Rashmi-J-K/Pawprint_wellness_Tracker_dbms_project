from flask import Flask, render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from datetime import datetime
from sqlalchemy import text

# db connection
local_server = True

app = Flask(__name__, template_folder='templates')


login_manager = LoginManager(app)
login_manager.login_view='login'
app.secret_key = 'RakshitaYaji'
@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))
# Correct the configuration name to SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pet'
db = SQLAlchemy(app)




class Login(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    empid=db.Column(db.String(50))
    password=db.Column(db.String(1000))



# creating db model (db tables)
class Pet(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True)
    breed = db.Column(db.String(50))
    age = db.Column(db.Integer)  # Corrected from db.Int(2)
    species = db.Column(db.String(50))
    u_id = db.Column(db.String(50))

class health_record(db.Model):
    record_id=db.Column(db.Integer,primary_key=True)
    pet_id=db.Column(db.Integer)
    vaccination=db.Column(db.String(100))
    medication=db.Column(db.String(100))
    medical_history=db.Column(db.String(100))


class nutrition_and_diet(db.Model):
    nutrition_diet_id=db.Column(db.Integer,primary_key=True)
    pet_id=db.Column(db.Integer)
    diet_plan=db.Column(db.String(100))
    requirements=db.Column(db.String(100))



class emergency_contact(db.Model):
    contact_id=db.Column(db.Integer,primary_key=True)
    pet_relation=db.Column(db.String(50))
    name=db.Column(db.String(50))
    pet_id=db.Column(db.Integer)
    phone=db.Column(db.String(10))



class appointment(db.Model):
    ap_id=db.Column(db.Integer,primary_key=True)
    pet_id=db.Column(db.Integer)
    date=db.Column(db.Date)
    purpose=db.Column(db.String(100))
    notes=db.Column(db.String(100))











@app.route('/')
  
def index():
    return render_template('index.html')
@app.route('/home')    


@app.route('/appointment',methods=['POST','GET'])
@login_required 
def appointment():
    if request.method =="POST":
        # pet_id=request.form.get('pet_id')
        pet_id=request.form.get('pet_id')
        date=request.form.get('date')
        purpose=request.form.get('purpose')
        notes=request.form.get('notes')

        query = text(
            f"INSERT INTO appointment (pet_id, date, purpose, notes) VALUES ('{pet_id}', '{date}', '{purpose}', '{notes}');"
        )
        db.session.execute(query)
        db.session.commit()

        flash("appointment details added","success")
        return redirect(url_for('index'))
    return render_template('appointment.html')


@app.route('/healthrecord',methods=['POST','GET'])   
@login_required 
def healthrecord():
    if request.method =="POST":
        # pet_id=request.form.get('pet_id')
        pet_id=request.form.get('pet_id')
        vaccination=request.form.get('vaccination')
        medication=request.form.get('medication')
        medical_history=request.form.get('medical_history')

        query = text(
            f"INSERT INTO health_record (pet_id, vaccination, medication,medical_history) VALUES ('{pet_id}', '{vaccination}', '{medication}', '{medical_history}');"
        )
        db.session.execute(query)
        db.session.commit()

        flash("health record details added","success")
        return redirect(url_for('index'))

    return render_template('healthrecord.html')



@app.route('/nutrition')
@login_required 
def nutrition():
    return render_template('nutrition.html')



@app.route('/contact',methods=['POST','GET'])
@login_required 
def contact():
    if request.method =="POST":
        # pet_id=request.form.get('pet_id')
        pet_relation=request.form.get('pet_relation')
        name=request.form.get('name')
        pet_id=request.form.get('pet_id')
        phone=request.form.get('phone')

        query = text(
            f"INSERT INTO emergency_contact (pet_relation, name, pet_id, phone) VALUES ('{pet_relation}', '{name}', '{pet_id}', '{phone}');"
        )

        # Use db.engine.execute to execute the textual SQL expression
        db.session.execute(query)
        db.session.commit()

        flash("contact details added","success")
        return redirect(url_for('index'))

    return render_template('contact.html')



@app.route('/pet_register',methods=['POST','GET'])
def register():
    if request.method =="POST":
        # pet_id=request.form.get('pet_id')
        breed=request.form.get('breed')
        age=request.form.get('age')
        species=request.form.get('species')
        unique_id=request.form.get('unique_id')

        query = text(
            f"INSERT INTO pet (breed, age, species, u_id) VALUES ('{breed}', '{age}', '{species}', '{unique_id}');"
        )

        # Use db.engine.execute to execute the textual SQL expression
        db.session.execute(query)
        db.session.commit()

        flash("Pet details added","success")
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/pet_add',methods=['GET'])
def view():
    query = text("SELECT * FROM pet;")
    query_result = db.session.execute(query)

    # Fetch all rows from the query result
    pet_data = query_result.fetchall()

    # No need to commit when reading data
    # db.session.commit()
    print(pet_data)

    return render_template('view.html', pet_data=pet_data)





@app.route('/login', methods=['POST','GET'])
def login():
    if request.method =="POST":
        empid=request.form.get('empid')
        password=request.form.get('password')
        if(len(password)<8 or len(password)>25):
            flash("Password must be atleast 8 characters long","danger")
            return render_template('login.html')
        login=Login.query.filter_by(empid=empid,password=password).first()
        if login:
            login_user(login)
            flash("Login successful","success")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')
    
    return render_template('login.html')





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/edit/pet/<string:pet_id>", methods=['POST','GET'])
@login_required
def epet(pet_id):
    post = Pet.query.filter_by(pet_id=pet_id).first()
    if request.method == "POST":
       breed = request.form.get('breed')
       age = request.form.get('age')
       species = request.form.get('species')
       unique_id = request.form.get('unique_id')
       print(f"Received form data: breed={breed}, age={age}, species={species}, unique_id={unique_id}")

       query = f"UPDATE Pet SET breed='{breed}', age='{age}', species='{species}', unique_id='{unique_id}' WHERE pet_id={pet_id};"
       db.session.execute(query)
       db.session.commit()
       flash("Updated", "success")
       return redirect('/view')

    return render_template('edit_pet.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
