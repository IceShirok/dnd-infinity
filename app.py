from flask import Flask, render_template, redirect, url_for, abort, flash
from ddddd import pc_playground as pc
from ddddd.entity.character.base import prettify_modifier

import logging

from ddddd.mechanics import dice
from ddddd.pc_creator import PcCreatorForm

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


app = Flask(__name__)
app.config.from_object(Config)

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


@app.route('/pc/create', methods=['GET', 'POST'])
def create_pc():
    form = PcCreatorForm()
    if form.validate_on_submit():
        flash('name : {}'.format(form.name.data))
        flash('race : {}'.format(form.race.data))
        flash('vocation : {}'.format(form.vocation.data))
        flash('background : {}'.format(form.background.data))

        ability_scores = {
            'STR': dice.roll_ability_score(),
            'DEX': dice.roll_ability_score(),
            'CON': dice.roll_ability_score(),
            'INT': dice.roll_ability_score(),
            'WIS': dice.roll_ability_score(),
            'CHA': dice.roll_ability_score(),
        }
        flash(ability_scores)

    return render_template('creation/pc_creator.html',
                           title='D&D Character Creation - Create',
                           form=form)


@app.route('/pc/create/race', methods=['GET', 'POST'])
def create_pc_race():
    return render_template('creation/race.html',
                           title='D&D Character Creation - Race',
                           next_url=url_for('create_pc_vocation'))


@app.route('/pc/create/vocation', methods=['GET', 'POST'])
def create_pc_vocation():
    return render_template('creation/vocation.html',
                           title='D&D Character Creation - Vocation',
                           prev_url=url_for('create_pc_race'),
                           next_url=url_for('create_pc_abilities'))


@app.route('/pc/create/abilities', methods=['GET', 'POST'])
def create_pc_abilities():
    ability_scores = {
        'STR': dice.roll_ability_score(),
        'DEX': dice.roll_ability_score(),
        'CON': dice.roll_ability_score(),
        'INT': dice.roll_ability_score(),
        'WIS': dice.roll_ability_score(),
        'CHA': dice.roll_ability_score(),
    }

    return render_template('creation/abilities.html',
                           title='D&D Character Creation - Abilities',
                           ability_scores=ability_scores,
                           prev_url=url_for('create_pc_vocation'),
                           next_url=url_for('create_pc_background'))


@app.route('/pc/create/background', methods=['GET', 'POST'])
def create_pc_background():
    return render_template('creation/background.html',
                           title='D&D Character Creation - Background',
                           prev_url=url_for('create_pc_abilities'))


if __name__ == '__main__':
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)
    app.run(host='localhost')
