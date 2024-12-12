from .app import app
from flask import render_template
from .utils.format import jsonify
from .utils import logging
import os
import uuid
from flask import request
from . import database


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', environment=os.environ['environment'])


@app.route("/quizz")
def quizz():
    return render_template('quizz.html', environment=os.environ['environment'])


@app.route("/liveness_check")
def liveness_check():
    return "ok"


@app.route("/readiness_check")
def readiness_check():
    return "ok"


@app.route("/is_logged_in", methods=['POST'])
def is_logged_in():
    return jsonify({'is_logged_in':False})


@app.route("/get_new_anonymous_user_id", methods=['POST'])
def get_new_anonymous_user_id():
    user_id = database.add_anonymous_user()
    return jsonify({'value':user_id})


@app.route("/get_anonymous_question", methods=['POST'])
def get_anonymous_question():
    return jsonify(database.get_anonymous_question(request.json)[0])


@app.route("/set_anonymous_answer", methods=['POST'])
def set_anonymous_answer():
    database.set_anonymous_answer(request.json)
    return jsonify({'ok':'ok'})


@app.route("/get_anonymous_ranking", methods=['POST'])
def get_anonymous_ranking():
    return jsonify(database.get_anonymous_ranking(request.json))


@app.route("/get_anonymous_ranking_2", methods=['POST'])
def get_anonymous_ranking_2():
    return jsonify(database.get_anonymous_ranking_2(request.json))


@app.route("/reset_anonymous_option", methods=['POST'])
def reset_anonymous_option():
    return jsonify(database.reset_anonymous_option(request.json))


@app.route("/get_anonymous_matches", methods=['POST'])
def get_anonymous_matches():
    return jsonify(database.get_anonymous_matches(request.json))
