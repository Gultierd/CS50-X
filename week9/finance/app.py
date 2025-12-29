import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT symbol, SUM(amount) AS [shares], price, total FROM stocks WHERE userID = ? GROUP BY symbol;", session["user_id"]
    )
    # getting all stocks exchanges in users history
    username = db.execute(
        "SELECT username FROM users WHERE id = ?", session["user_id"]
    )
    # getting username
    i = 0
    total = 0
    while i < len(stocks):
        if stocks[i]["shares"] < 1:
            stocks.pop(i)
            i = i-1
            # if user sold all his shares of given stock we do not display it in index
        else:
            currentStock = lookup(stocks[i]["symbol"])
            total = total + float(currentStock["price"] * stocks[i]["shares"])
            stocks[i]["price"] = usd(currentStock["price"])
            stocks[i]["total"] = usd(currentStock["price"] * stocks[i]["shares"])
            i = i+1
            # we update stock price to current data using lookup
        # changing all finance related fields to dollars
    cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"]
    )
    total = total + float(cash[0]["cash"])
    return render_template("index.html", username=username[0]["username"], stocks=stocks, cash=usd(cash[0]["cash"]), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html", info="")
    else:
        # Ensure both stock symbol and amount was submitted
        shares = request.form.get("shares")
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        elif not shares:
            return apology("must provide share amount", 400)

        if not shares.isnumeric() or int(shares) < 1:
            return apology("invalid share amount", 400)

        stock = lookup(request.form.get("symbol"))
        # searching for given stock
        if not stock:
            return apology("must provide stock symbol", 400)
            # if symbol does not exist
        else:
            # stock exists - now checking for cash in our account
            total = stock["price"] * int(shares)
            cash = db.execute(
                "SELECT cash FROM users WHERE id = ?", session["user_id"]
            )
            if total > cash[0]["cash"]:
                inf = "Not enough funds!"
            else:
                cash[0]["cash"] = cash[0]["cash"] - total
                db.execute(
                    "UPDATE users SET cash = ? WHERE id = ?", cash[0]["cash"], session["user_id"]
                )
                # updating cash in database

                # inf = (
                #   f"Bought {shares} shares of {stock["name"]} ({stock["symbol"]}) for {usd(total)} - new cash total is {usd(cash[0]["cash"])}")
                # information for user, visible on page - REMOVED, NOW BUYING REDIRECTS USER TO HOME PAGE

                db.execute(
                    "INSERT INTO stocks (userID, symbol, amount, price, total, time) VALUES (?, ?, ?, ?, ?, ?)",
                    session["user_id"], stock["symbol"], request.form.get("shares"),
                    stock["price"], total, datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                # adding data to stocks table, using imported datetime library to get current date

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute(
        "SELECT * FROM stocks WHERE userID = ?", session["user_id"]
    )
    # getting all stocks exchanges in users history
    username = db.execute(
        "SELECT username FROM users WHERE ID = ?", session["user_id"]
    )
    # getting username
    for i in range(len(stocks)):
        stocks[i]["price"] = usd(stocks[i]["price"])
        stocks[i]["total"] = usd(stocks[i]["total"])
        # changing all finance related fields to dollars
    return render_template("history.html", username=username[0]["username"], stocks=stocks)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """User changes his password"""

    if request.method == "GET":
        return render_template("password.html")
        # route via get, show user the fields
    else:
        oldPassword = db.execute(
            "SELECT hash FROM users WHERE id = ?", session["user_id"]
        )
        if not request.form.get("oldPassword") or not request.form.get("newPassword1") or not request.form.get("newPassword2"):
            return apology("must fill all fields above", 403)
        # make sure user provides input to all fields above

        elif not check_password_hash(
            oldPassword[0]["hash"], request.form.get("oldPassword")
        ):
            return apology("password is incorrect", 403)
        # make sure the old password is correct

        elif request.form.get("newPassword1") != request.form.get("newPassword2"):
            return apology("passwords do not match", 403)
        # and that provided new passwords are the same values

        elif request.form.get("newPassword1") == request.form.get("oldPassword"):
            return apology("new password must be different", 403)
        # and that new password is different from previous one

        # if all values are correct we can update the database
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
                request.form.get("newPassword1")), session["user_id"]
        )

        # Redirect user to log in once again
        return redirect("/logout")


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
    if request.method == "GET":
        return render_template("quote.html", quote="")
    # rendering first template, prompting user for symbol
    else:
        q = ""
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
            # if user does not provide any symbol
        else:
            stock = lookup(request.form.get("symbol"))
            if not stock:
                return apology("must provide valid symbol", 400)
                # if symbol does not exist
            else:
                q = (f"Share of {stock["name"]} ({stock["symbol"]}) costs {usd(stock["price"])}")
                # symbol exists, we take data from lookup method
        return render_template("quote.html", quote=q)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide same password twice", 400)
        # same as during log in - checking for requested data

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        # checking if the passwords match

        name = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(name) != 0:
            return apology("username already in use", 400)
        # checking if the username is used

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password"))
        )
        # creating new database entry

        id = db.execute(
            "SELECT id FROM users WHERE username = ?", request.form.get("username")
        )
        # getting id for session

        session["user_id"] = id[0]["id"]
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():  # todo
    stocks = db.execute(
        "SELECT symbol, SUM(amount) AS [shares] FROM stocks WHERE userID = ? GROUP BY symbol", session["user_id"]
    )

    symbols = []
    for i in range(len(stocks)):
        if stocks[i]["shares"] > 0:
            symbols.append(stocks[i]["symbol"])
        # getting all user related symbols if they have any in their portfolio

    if request.method == "GET":
        return render_template("sell.html", symbols=symbols)
        # rendering a template for user

    else:
        inputSymbol = request.form.get("symbol")
        inputShares = request.form.get("shares")
        # shortcuts to all request forms from user
        userShares = db.execute(
            "SELECT SUM(amount) FROM stocks WHERE userID = ? AND symbol = ?", session["user_id"], inputSymbol
        )
        # getting data on shares that user has

        if not inputSymbol or inputSymbol not in symbols:
            return apology("must provide correct stock symbol", 400)

        elif (not inputShares) or (int(inputShares) < 1) or (int(inputShares) > userShares[0]["SUM(amount)"]):
            return apology("must provide correct share amount", 400)
        # apologies for not giving any inputs, when symbol is not in users possesion or amount is too large or too small

        # all data correct - updating our database now
        stock = lookup(inputSymbol)
        # searching for given stock for its current price
        total = stock["price"] * int(inputShares)
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )

        cash[0]["cash"] = cash[0]["cash"] + total
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", cash[0]["cash"], session["user_id"]
        )
        # updating our users cash data from selling stocks

        db.execute(
            "INSERT INTO stocks (userID, symbol, amount, price, total, time) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"], stock["symbol"], (int(inputShares) * -1),
            stock["price"], total, datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        # updating our users stocks data, inserting into his history

        return redirect("/")
