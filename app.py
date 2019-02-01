from flask import Flask, render_template, redirect
from ddddd import pc_playground as pc
from ddddd.entity.base import prettify_modifier

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/1')


@app.route('/<int:level>')
def create_dorian(level):
    return render_template('character_sheet.html',
                           title='D&D Character Sheet',
                           pc=pc.create_dorian(level=level),
                           pmod=prettify_modifier)


if __name__ == '__main__':
    app.run(host='localhost')
