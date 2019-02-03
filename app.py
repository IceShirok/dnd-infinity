from flask import Flask, render_template, redirect
from ddddd import pc_playground as pc
from ddddd.entity.base import prettify_modifier

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           title='D&D Character Sheet')


@app.route('/pc/<string:pc_name>')
def create_tamiphi_def():
    return redirect('/pc/<string:pc_name>/1')


@app.route('/pc/<string:pc_name>/<int:level>')
def generate_pc(pc_name, level):
    create_pc = None
    if pc_name == 'dorian':
        create_pc = pc.create_dorian
    elif pc_name == 'tamiphi':
        create_pc = pc.create_tamiphi
    elif pc_name == 'fethri':
        create_pc = pc.create_fethri
    else:
        redirect('/')
    return render_template('character_sheet.html',
                           title='D&D Character Sheet - {}'.format(pc_name),
                           pc=create_pc(level=level),
                           pmod=prettify_modifier)


if __name__ == '__main__':
    app.run(host='localhost')
