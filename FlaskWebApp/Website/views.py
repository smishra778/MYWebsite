import json
import os
import subprocess

from flask import Blueprint, jsonify, redirect, url_for
from flask import render_template, flash, request
from flask_login import login_required, current_user

from . import db, Sudoku
from .models import Note

views = Blueprint('views', __name__)


@views.route('/')
def welcome():
    if current_user.is_authenticated > 0:
        return render_template("home.html", user=current_user)
    else:
        return redirect(url_for('auth.login'))


@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully', category='success')

    return render_template('notes.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/sudoku-solve', methods=['POST', 'GET'])
def sudoku():
    input_values = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    if request.method == 'POST':
        # Get input data and parse it into a list of lists

        input_data = request.form.to_dict()
        print(input_data)
        puzzle = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = input_data.get(f'cell-{i}-{j}')
                if cell:
                    row.append(int(cell))
                else:
                    row.append(0)
            # print(row)
            puzzle.append(row)

        # Solve the puzzle
        solution = Sudoku.sudoku_solve(puzzle)
        solution_final = jsonify({'solution': solution})
        print(solution_final)
        # Render the template with the solved puzzle
        return jsonify({'solution': solution})

    # If it's a GET request, just render the template
    return render_template('sudoku.html', user=current_user, input_values=input_values)


@views.route('/spaceinvader', methods=['POST', 'GET'])
def run_space_invader():
    subprocess.Popen(r"C:\Users\shubh\PycharmProjects\FlaskWebApp\Website\Space Invader\exe.win32-3.8\main.exe")
    return redirect(url_for('views.home'))
