from flask import Flask, request, render_template, redirect, url_for , session

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
def index():
	if("username" in session.keys()):
		return render_template('welcome.html', login = "True")

	else:
		return render_template('welcome.html', login = "False")

@app.route("/login", methods = ['POST'])
def login():
	if(request.form["password"] == "pachi" and request.form["username"] == "Prashanth"):
		print("login successful. Redirecting to products page")
		session['username'] = request.form["username"]
		return redirect(url_for('index'))

	else:
		return render_template('error.html')

@app.route("/signup", methods =["POST"])
def signup():
	user_info = {}
	user_info["firstname"] = request.form["firstname"]
	user_info["lastname"] = request.form["lastname"]
	user_info["email"] = request.form["email"]
	user_info["password"] = request.form["password"]

	session['username'] = user_info
	return redirect(url_for('index'))
	
@app.route("/products")
def product_page():
	return render_template('products.html')

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

if(__name__ == "__main__"):
	app.run()

