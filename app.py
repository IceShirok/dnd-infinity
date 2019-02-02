from flask import Flask, render_template, redirect
from ddddd import pc_playground as pc
from ddddd.entity.base import prettify_modifier

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           title='D&D Character Sheet')


@app.route('/tamiphi')
def create_tamiphi_def():
    return redirect('/tamiphi/1')


@app.route('/tamiphi/<int:level>')
def create_tamiphi(level):
    return render_template('character_sheet.html',
                           title='D&D Character Sheet - Tamiphi',
                           pc=pc.create_tamiphi(level=level),
                           pmod=prettify_modifier)


@app.route('/dorian')
def create_dorian_def():
    return redirect('/dorian/5')


@app.route('/dorian/<int:level>')
def create_dorian(level):
    return render_template('character_sheet.html',
                           title='D&D Character Sheet - Dorian',
                           pc=pc.create_dorian(level=level),
                           pmod=prettify_modifier)


if __name__ == '__main__':
    app.run(host='localhost')
