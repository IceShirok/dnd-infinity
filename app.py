from flask import Flask, render_template, url_for
from ddddd import app as pc

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('character_sheet.html',
                           title='D&D Character Sheet',
                           pc=pc.create_dorian())


if __name__ == '__main__':
    app.run(host='localhost')
