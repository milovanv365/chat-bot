import os

from flask import Flask, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = '\xb8\xdaZ\xe71\xa7\x16\xa1\x144F\x15\xf6\x97\xee\x98\xf6\xad\xab\xcb\xdfxra'


@app.route("/")
def index_view():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True,
    )
