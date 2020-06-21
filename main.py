import os

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config["SECRET_KEY"] = "\xb8\xdaZ\xe71\xa7\x16\xa1\x144F\x15\xf6\x97\xee\x98\xf6\xad\xab\xcb\xdfxra"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI") or \
                                        "sqlite:///" + os.path.join(ROOT_DIR, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from dbmodels import Customer, Product, Account


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Customer": Customer,
        "Product": Product,
        "Account": Account
    }


@app.route("/", methods=["GET", "POST"])
def index_view():
    if request.method == "POST":
        question = request.values["question"]
        response = {"status": "success"}
        return jsonify(response)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
    )
