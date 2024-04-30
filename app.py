from flask import Flask, render_template, request, redirect, url_for, jsonify
from uuid import uuid4
from datetime import datetime
app = Flask(__name__)

URGENCY_THRESHOLD_DAYS = {
    'immediate': 0,
    'very_high': 2,
    'high': 3,
    'medium': 7,
    'low': 14
}

URGENCY_SCORES = {
    'immediate': 10,
    'very_high': 9,
    'high': 8,
    'medium': 6,
    'low': 4,
    'none': 2
}


def calculate_urgency(deadline):
    today = datetime.today().date()
    try:
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
    except ValueError:
        return URGENCY_SCORES['none']

    days_to_deadline = (deadline_date - today).days

    for threshold, score in URGENCY_SCORES.items():
        if days_to_deadline <= URGENCY_THRESHOLD_DAYS.get(threshold, float('inf')):
            return score


def calculate_priority(importance, urgency, estimated_time):
    return (importance + urgency) / estimated_time


def create_task(name, importance, deadline, estimated_time):
    urgency = calculate_urgency(deadline)
    priority = calculate_priority(int(importance), urgency, int(estimated_time))
    return {
        "id": str(uuid4()),
        "name": name,
        "completed": False,
        "importance": int(importance),
        "urgency": urgency,
        "priority": priority,
        "deadline": deadline,
        "estimated_time": int(estimated_time)
    }


todos = []


@app.route('/')
def todo_list():
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add_todo():
    task_name = request.form.get('task')
    task_importance = request.form.get('importance', 5)
    task_deadline = request.form.get('deadline')
    task_estimated_time = request.form.get('estimated_time', 1)

    new_task = create_task(task_name, task_importance, task_deadline, task_estimated_time)
    todos.append(new_task)
    todos.sort(key=lambda x: x['priority'])
    return redirect(url_for('todo_list'))


@app.route('/toggle/<task_id>', methods=['GET'])
def toggle_task(task_id):
    for task in todos:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    return '', 204  # Kod statusu 204 No Content


@app.route('/sort/<sort_by>')
def sort_tasks(sort_by):
    sort_key = {
        "priority": lambda x: x['priority'],
        "name": lambda x: x['name'],
        "importance": lambda x: x['importance'],
        "urgency": lambda x: x['urgency']
    }.get(sort_by, lambda x: x['priority'])
    todos.sort(key=sort_key, reverse=sort_by != "name")
    return jsonify(todos)


if __name__ == '__main__':
    app.run(debug=True)