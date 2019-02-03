from flask import Flask, render_template, redirect, url_for, abort
from ddddd import pc_playground as pc
from ddddd.entity.base import prettify_modifier

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           title='D&D Character Sheet')


@app.errorhandler(500)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('lost.html',
                           available_pc=pc.get_available_characters()), 404


@app.route('/pc/<string:pc_name>')
def generate_pc_def():
    return redirect(url_for('generate_pc', pc_name=pc, level=1))


@app.route('/pc/<string:pc_name>/<int:level>')
def generate_pc(pc_name, level):
    available_pc = pc.get_available_characters()
    create_pc = None
    if pc_name in available_pc:
        create_pc = available_pc[pc_name]['create']
    if not create_pc:
        abort(404)
    return render_template('character_sheet.html',
                           title='D&D Character Sheet - {}'.format(pc_name.capitalize()),
                           pc=create_pc(level=level),
                           pmod=prettify_modifier)


if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    app.run(host='localhost')
