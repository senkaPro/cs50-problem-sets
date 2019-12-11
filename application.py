import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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
    return render_template("layout.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        data = lookup(symbol)
        shares = int(request.form.get("shares"))

        if shares <= 0:
            return apology("Must provide positive number of shares")

        if data == None:
            return apology("Invalid symbol")

        price = data["price"]
        total_amount = price * shares

        user = db.execute("SELECT cash FROM users WHERE id= :user_id",user_id=session["user_id"])
        cash = user[0]["cash"]
        if cash >= total_amount:
            trans = db.execute("INSERT INTO transactions (user_id,stock,quantity,price_bought) \
                                        VALUES ( :user_id, :stock, :quantity, :price)",
                        user_id = session["user_id"],
                        stock = symbol,
                        quantity = shares,
                        price = price)
            if trans == None:
                return apology("Cannot finish transaction")

            user = db.execute("UPDATE users SET cash = cash - :amount WHERE id = :id",
                                amount = total_amount,
                                id = session["user_id"])

            flash("Successful transaction!")
        return render_template("layout.html")

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
        session["username"] = rows[0]["username"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get('symbol')

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
        if not password:
            return apology("Please provide a password")
        if not confirmation:
            return apology("Confirm your password")
        if password != confirmation:
            return apology("Your passwords don't match")

        hash = generate_password_hash(password)

        user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",username=username, hash=hash)
        if user == None:
            return apology("User already exist!")
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        flash("You successfuly registered!")
        return render_template('layout.html')
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
