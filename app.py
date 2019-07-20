from flask import Flask, render_template, redirect, url_for, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from ddddd import pc_playground as pc
from ddddd.entity.character.base import prettify_modifier

import logging
import os

from ddddd.mechanics import init_tracker

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


@app.route('/')
def index():
    return render_template('index.html',
                           title='D&D Character Sheet')


@app.errorhandler(500)
def server_error(e):
    logger.error(e)
    return render_template('broken.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    logger.error(e)
    return render_template('lost.html',
                           available_pc=pc.get_available_characters()), 404


"""
PC Character Manager
"""


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


"""
Initiative Tracker
"""


@app.route('/combat/create')
def initiative_tracker_creator():
    return render_template('init_tracker_creator.html',
                           title='D&D Initiative Tracker')


it = init_tracker.get_sample_initiative_tracker()
it.reset_combat()


@app.route('/combat')
def initiative_tracker():
    return render_template('init_tracker.html',
                           title='D&D Initiative Tracker',
                           init_tracker=it)


@app.route('/combat/next')
def initiative_tracker_next_turn():
    it.next_turn()
    return redirect(url_for('initiative_tracker'))


@app.route('/combat/reset')
def initiative_tracker_reset():
    it.reset_combat()
    return redirect(url_for('initiative_tracker'))


if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)
    app.run(host='localhost')
