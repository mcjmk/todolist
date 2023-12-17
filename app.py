from flask import Flask, render_template, request, redirect, url_for, jsonify
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)


def calculate_urgency(deadline):
    today = datetime.today().date()
    deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
    days_to_deadline = (deadline_date - today).days

    if days_to_deadline < 0:
        return 10
    elif days_to_deadline < 2:
        return 9
    elif days_to_deadline < 3:
        return 8
    elif days_to_deadline < 7:
        return 6
    elif days_to_deadline < 14:
        return 4
    else:
        return 2


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
    global todos

    if sort_by == "priority":
        sorted_todos = sorted(todos, key=lambda x: x['priority'], reverse=True)
    elif sort_by == "name":
        sorted_todos = sorted(todos, key=lambda x: x['name'])
    elif sort_by == "importance":
        sorted_todos = sorted(todos, key=lambda x: x['importance'], reverse=True)
    elif sort_by == "urgency":
        sorted_todos = sorted(todos, key=lambda x: x['urgency'], reverse=True)
    else:
        sorted_todos = todos

    return jsonify(sorted_todos)

if __name__ == '__main__':
    app.run(debug=True)