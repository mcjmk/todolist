from flask import Flask, render_template, request, redirect, url_for, jsonify
from uuid import uuid4

app = Flask(__name__)

def create_task(name, importance=5, urgency=5):
    return {
        "id": str(uuid4()),
        "name": name,
        "completed": False,
        "importance": int(importance),
        "urgency": int(urgency)
    }



todos = []

@app.route('/')
def todo_list():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task_name = request.form.get('task')
    task_importance = request.form.get('importance', 5)  # Domyślna wartość to 5
    task_urgency = request.form.get('urgency', 5)  # Domyślna wartość to 5
    new_task = create_task(task_name, task_importance, task_urgency)
    todos.append(new_task)
    todos.sort(key=lambda x: x['name'])
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
    if sort_by == "name":
        todos = sorted(todos, key=lambda x: x['name'])
    elif sort_by == "importance":
        todos = sorted(todos, key=lambda x: x['importance'], reverse=True)
    elif sort_by == "urgency":
        todos = sorted(todos, key=lambda x: x['urgency'], reverse=True)

    return jsonify(todos)

if __name__ == '__main__':
    app.run(debug=True)