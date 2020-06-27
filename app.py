import os

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from engine.engine import get_query_data

app = Flask(__name__)

app.config["SECRET_KEY"] = "\xb8\xdaZ\xe71\xa7\x16\xa1\x144F\x15\xf6\x97\xee\x98\xf6\xad\xab\xcb\xdfxra"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:rootroot@localhost/chat_bot_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# from dbmodels import Accounts
#
#
# @app.shell_context_processor
# def make_shell_context():
#     return {
#         "db": db,
#         "Account": Accounts
#     }


@app.route("/", methods=["GET", "POST"])
def index_view():
    if request.method == "POST":
        question = request.values["question"]
        query_data = get_query_data(question)

        # query_sql = "select balance from accounts where account_number = 123456"
        if query_data['condition_value'] is not None:
            query_sql = "select %s from accounts where %s = '%s'" % (
                query_data['target_field'], query_data['condition_field'], query_data['condition_value'])
        else:
            query_sql = "select %s from accounts group by %s" % (
                query_data['target_field'], query_data['condition_field'])

        try:
            query_result = db.engine.execute(query_sql)
            results = []
            for row in query_result:
                results.append(row[0])

            response = {
                "status": "success",
                "answer": results
            }
        except Exception as e:
            response = {
                "status": "fail"
            }

        return jsonify(response)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
    )
