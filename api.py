from flask import Flask, request, render_template, redirect, url_for , session
from models.user_model import user_signup , search_user_by_username, Product_addition , check_user , seller_products , buyer_products, search_user_by_user_id, cart_details, update_cart_details, search_products_in_page

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
def index():
	if("user_id" in session.keys()):
		return render_template('welcome.html', login = "True")

	else:
		return render_template('welcome.html', login = "False")

@app.route("/login", methods = ['POST'])
def login():
	inbound_username = request.form["username"]
	existing_user = search_user_by_username(inbound_username)
	if(existing_user is None):
		return render_template('error.html', message = "You have to sign up first")

	elif(request.form["password"] == existing_user["password"]):
		print("login successful. Redirecting to products page")
		session['user_id'] = str(existing_user['_id'])
		session['accounttype'] = str(existing_user['accounttype'])
		return redirect(url_for('index'))

	else:
		return render_template('error.html', message = "user name or password incorrect")

@app.route("/signup", methods =["POST"])
def signup():
	user_info = {}
	user_info["username"] = request.form["username"]
	user_info["name"] = request.form["name"]
	user_info["email"] = request.form["email"]
	user_info["password"] = request.form["password"]
	user_info["accounttype"] = request.form["accounttype"]	
	#import pdb; pdb.set_trace()
	if check_user(user_info["username"]) is None:
		results = user_signup(user_info)
		if(results is True):
			session['user_id'] = str(user_info['_id'])
		return("Successfully saved")

	else:
		return "IT Exists"	
	#return redirect(url_for('index'))
	
@app.route("/products")
def product_page():
	if session["accounttype"] == "seller":
		result = seller_products(session["user_id"])
	else:
		result = buyer_products()
	for value in result:
		seller_id = value.get("seller_id")
		seller_object = search_user_by_user_id(seller_id)
		seller_username = seller_object["username"]
		value["seller_username"] = seller_username
	return render_template('products.html', result=result)

@app.route("/Add_products", methods = ["POST"])
def Add_product_page():
	product_info = {}
	product_info["product name"] = request.form["name"]
	product_info["price"] = request.form["price"]
	product_info["product description"] = request.form["product_description"]
	product_info["seller_id"] = session["user_id"]
	results = Product_addition(product_info)
	return 'product added'

@app.route("/Add_products", methods = ["GET"])
def product():
	return render_template('Add_products.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id =request.form["product_id"]
    update_cart_details(session["user_id"],product_id)
    return redirect(url_for("product_page"))

@app.route('/cart_page')
def cart_page():
    cart= cart_details(session["user_id"])
    print(cart)
    return render_template("cart_page.html",cart=cart)

@app.route("/searchproducts", methods=["POST"])
def search_products():
	word = request.form["search"]
	search = search_products_in_page(word)
	if search is None:
		return "No products found"

	else:
		return render_template("searchproducts.html",search=search)

@app.route('/logout')
def logout():
   session.pop('user_id', None)
   return redirect(url_for('index'))

if(__name__ == "__main__"):
	app.run(debug=True)
	

