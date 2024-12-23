import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from decimal import Decimal

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


@app.route("/finance/")
@login_required
def index():

    user_id = session["user_id"]
    database = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price, printf('%.2f', SUM(total)) AS total FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash_data = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = round(Decimal(cash_data[0]["cash"]), 2)

    stocks = db.execute("SELECT symbol, shares, total FROM transactions WHERE user_id = ?", user_id)

    worth = 0

    for row in stocks:
        worth = Decimal(worth) + Decimal(row["total"])

    worth = round(worth + Decimal(cash), 2)

    return render_template("index.html", database=database, cash=cash, worth=worth)


@app.route("/finance/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol required")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Invalid share value")

        if not shares:
            return apology("Shares required")

        if shares < 0:
            return apology("Invalid share value")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Stock not found")

        cost = shares * stock["price"]

        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = user_cash[0]["cash"]

        if cash < cost:
            return apology("Not enough money")

        new_cash = cash - cost

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)

        date = datetime.datetime.now()

        price = str(round(Decimal(stock["price"]), 2))

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total, date) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, price, cost, date)

        flash("Bought!")

        return redirect("/finance/")
    else:
        return render_template("buy.html")


@app.route("/finance/history")
@login_required
def history():
    user_id = session["user_id"]
    database = db.execute(
        "SELECT symbol, shares, price, date FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", database=database)


@app.route("/finance/login", methods=["GET", "POST"])
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
        return redirect("/finance/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/finance/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/finance/login")


@app.route("/finance/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Symbol required")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Stock not found")

        return render_template("quoted.html", price=round(Decimal(stock["price"]), 2), symbol=stock["symbol"])
    else:
        return render_template("quote.html")


@app.route("/finance/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Username required")

        password = request.form.get("password")
        if not password:
            return apology("Password required")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("Confirmation password required")

        if password != confirmation:
            return apology("Passwords do not match")

        hash = generate_password_hash(password)

        try:
            new = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username unavailable")

        session["user_id"] = new

        return redirect("/finance/")
    else:
        return render_template("register.html")


@app.route("/finance/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol required")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Invalid share value")

        if shares < 0:
            return apology("Invalid share value")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Stock not found")

        value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = user_cash[0]["cash"]

        user_shares = db.execute(
            "SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)
        u_shares = user_shares[0]["shares"]

        if shares > u_shares:
            return apology("Not enough shares")

        new_cash = cash + value
        shares = shares * -1

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)

        date = datetime.datetime.now()
        total = stock["price"] * shares

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total, date) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"], total, date)

        flash("Sold!")

        return redirect("/finance/")
    else:
        user_id = session["user_id"]
        user_symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares)", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in user_symbols])


@app.route("/finance/cash", methods=["GET", "POST"])
@login_required
def cash():
    if request.method == "POST":
        try:
            cash = round(Decimal(request.form.get("cash")))
        except:
            return apology("Invalid cash value")

        if cash > 10000:
            return apology("Invalid cash value")

        if cash < 0:
            return apology("Invalid cash value")

        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        u_cash = user_cash[0]["cash"]

        new_cash = cash + u_cash

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)

        flash("Withdrawn!")

        return redirect("/finance/")
    else:
        return render_template("cash.html")

@app.route("/home")
def home():
    nothing = " "
    return render_template("home.html", nothing=nothing)

@app.route("/about")
def about():
    nothing = " "
    return render_template("about.html", nothing=nothing)

@app.route("/github")
def github():
    nothing = " "
    return render_template("github.html", nothing=nothing)

@app.route("/something")
def something():
    nothing = " "
    return render_template("something.html", nothing=nothing)

@app.route("/finance/leaderboard")
@login_required
def leaderboard():
    database2 = db.execute("SELECT username, cash FROM users GROUP BY cash LIMIT 10")
    return render_template("leaderboard.html", database2=database2)


@app.route("/chat/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        name = request.form.get("username")
        if not name:
            return render_template("chat.html")

        comment = request.form.get("comment")
        if not comment:
            return render_template("chat.html")

        name = "{}".format(name)
        comment = "{}".format(comment)

        if len(name) > 10:
            return render_template("chat.html")
        if len(comment) > 200:
            return render_template("chat.html")

        date = datetime.datetime.now()
        date = "{}".format(date)

        db.execute("INSERT INTO chat (name, comment, date) VALUES (?, ?, ?)", name, comment, date)

        database2 = db.execute("SELECT id, name, comment, date FROM chat ORDER BY id DESC LIMIT 20")

        return render_template("chat.html", database2=database2)
    else:
        return render_template("chat.html")
