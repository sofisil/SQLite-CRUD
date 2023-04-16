from flask import Flask, render_template, request, redirect, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# create the extension
# create the app

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize the app with the extension
#db.init_app(app)
db = SQLAlchemy(app)

#* DATABASE *#

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String(80))

    def __init__(self, username, email):
        self.username = username
        self.email = email

""" class User_1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    user_ci = db.Column(db.String)
    user_password = db.Column(db.String)
"""

#* ROUTES *#

@app.route("/")
def hello_world():
    nombre = "Sofi"
    return render_template("index.html", nombre=nombre)

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":        
        username = request.form["username"]
        email = request.form["email"]
        print(username)
        print(email)

        new_user = User(username, email)

        db.session.add(new_user)
        db.session.commit()
        #*Redirect: se hace un return temprano que te redirecciona a otro lado cuando se cumple la funcion
        #* url_for: te crea una direccion url para la funcion que le  url_for('el_nombre_de_la_funcion')
        return redirect(url_for('info_emprendedor'))

    return render_template("user/create.html")

@app.route("/info-emprendedor")
def info_emprendedor():
    return render_template('into-emprendedor.html')




#* use request methods *#
'''@app.route('/login', methods=['GET', 'POST'])

def create_user():
    if request.method =='POST':
        print("entre en post")
        print(request.form['name'])
        print(request.form['ci'])
        print(request.form['pass'])
        user = User_1(
            user_name = request.form['name'],
            user_ci = request.form['ci'],
            user_password = request.form['pass']
        )
        print(user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users'))

    return render_template("login.html")'''

@app.route('/admin')
def admin():
    users = User.query.all()
    print(users)
    return render_template('admin.html', users=users)


@app.route('/update', methods=["GET", "POST"])
def update():
	users = User.query.all()
	if request.method == 'POST':
		id = request.form['id_user']
		old_password = request.form['old_password']
		new_password = request.form['new_password']
		user = User.query.get(id) 
		print(user.email)

		if old_password == user.email:
			user.email = new_password
			db.session.add(user)
			db.session.commit()
			print("email changed")
		else:
			print("email's not the same")
	return render_template('update.html', users=users)

@app.route('/delete', methods=["GET", "POST"])
def delete():
	users = User.query.all()
	if request.method == 'POST':
		id = request.form['id_user']
		user = User.query.get(id)
		print(user)
		db.session.delete(user)
		db.session.commit()
		return redirect(url_for('delete'))
	return render_template('delete.html', users=users)

#* CREATE DATABASE *#
with app.app_context():
    db.create_all(bind_key='__all__')
#* RUN SERVER *#
if __name__ == "__main__":
    app.run(debug=True) #Ejecuta la aplicación Flask facilmente desde la terminal.

