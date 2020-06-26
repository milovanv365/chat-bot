import os

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from engine.text_analyze import get_query_data

app = Flask(__name__)

app.config["SECRET_KEY"] = "\xb8\xdaZ\xe71\xa7\x16\xa1\x144F\x15\xf6\x97\xee\x98\xf6\xad\xab\xcb\xdfxra"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:adminadmin@localhost/chat_bot_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from dbmodels import Accounts


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Account": Accounts
    }


@app.route("/", methods=["GET", "POST"])
def index_view():
    if request.method == "POST":
        question = request.values["question"]
        # query_data = get_query_data(question)

        query_sql = "select balance from accounts where account_number = 123456"
        result = db.engine.execute(query_sql)
        for row in result:
            data = row[0]
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
