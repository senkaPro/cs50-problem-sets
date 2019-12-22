import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""


    stocks = db.execute("SELECT * FROM transactions WHERE user_id= :id GROUP BY stock", id= session['user_id'])
    user = db.execute("SELECT * FROM users WHERE id = :id", id =session['user_id'])
    total = 0
    cur_price = {}
    for stock in stocks:
        cur_price[stock['stock']] = lookup(stock['stock'])
        total += cur_price[stock['stock']]['price'] * stock['quantity']

    total += user[0]['cash']

    return render_template("index.html", user=user[0], stocks=stocks, price=cur_price, total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        data = lookup(symbol)
        user = db.execute("SELECT cash FROM users WHERE id= :user_id",user_id=session["user_id"])
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("You must input a positive integer value")

        if shares <= 0:
            return apology("Must provide at least one quantity of shares")

        if not data:
            return apology("Invalid symbol")

        price = data["price"]
        total_amount = price * shares

        cash = user[0]["cash"]
        if total_amount > cash:
            return apology("Cannot finish transaction")

        trans = db.execute("INSERT INTO transactions (user_id,stock,quantity,price_bought) \
                                    VALUES ( :user_id, :stock, :quantity, :price)",
                                                    user_id = session["user_id"],
                                                    stock = symbol,
                                                    quantity = shares,
                                                    price = price)

        cash = db.execute("UPDATE users SET cash = cash - :amount WHERE id = :id",
                            amount = total_amount,
                            id = session["user_id"])

        flash("Successful transaction!")
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("stock.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user"] = rows
        # Redirect user to home page
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get('symbol').upper()

        data = lookup(symbol)

        if data == None:
            return apology("Invalid symbol")

        return render_template("quoted.html", data=data)

    if request.method == "GET":
        return render_template('quote.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please provide username")
        elif not password:
            return apology("Please provide a password")
        elif not confirmation:
            return apology("Confirm your password")
        elif password != confirmation:
            return apology("Your passwords don't match")

        hash = generate_password_hash(password)

        new_user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",username=username, hash=hash)
        if not new_user:
            return apology("User already exist!")
        session["user_id"] = new_user
        flash("You successfuly registered!")
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get('symbol')
        if not symbol:
            return apology("Invalid symbol!")
        try:
            shares = int(request.form.get('shares'))
            if shares <= 0:
                return apology("Must enter a positive number of shares")
        except:
            return apology("Invalid value of shares")
        data = lookup(symbol)
        price = data['price']
        total_price = shares * price
        tr = db.execute("SELECT * FROM transactions WHERE user_id= :user_id AND stock= :stock", user_id = session["user_id"], stock=symbol)
        if tr[0]['quantity'] < shares or tr[0]['quantity'] < 1:
            return apology('You don\'t have enough shares to sell')

        db.execute("UPDATE users SET cash= cash + :price WHERE id= :user_id", user_id=session['user_id'], price= total_price)

        db.execute("UPDATE transactions SET quantity= quantity - :quantity WHERE user_id= :user_id AND stock= :stock ", quantity= shares, user_id=session['user_id'], stock=symbol)
        trans = db.execute("SELECT * FROM transactions WHERE user_id = :id AND stock= :stock", id=session['user_id'], stock=symbol)
        print(trans)
            #db.execute("DELETE FROM transactions WHERE user_id= :id AND stock = :stock", id=session['user_id'], stock=symbol)
        return redirect(url_for('index'))
    else:
        q = db.execute("SELECT * FROM transactions WHERE user_id= :id ORDER BY quantity DESC", id= session['user_id'])
        return render_template("sell.html", q=q)
    return render_template("sell.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
