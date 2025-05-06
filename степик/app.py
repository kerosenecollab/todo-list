from flask import Flask, render_template, request, redirect, url_for
from database import create_connection, add_task, get_all_tasks, get_task_by_id, update_task, delete_task

app = Flask(__name__)

@app.route('/')
def index():
    conn = create_connection()
    tasks = get_all_tasks(conn)
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form.get('description', '')
    
    conn = create_connection()
    add_task(conn, title, description)
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    conn = create_connection()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        is_completed = True if request.form.get('is_completed') == 'on' else False
        
        update_task(conn, task_id, title, description, is_completed)
        conn.close()
        return redirect(url_for('index'))
    
    task = get_task_by_id(conn, task_id)
    conn.close()
    
    if task is None:
        return redirect(url_for('index'))
    
    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = create_connection()
    delete_task(conn, task_id)
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run(debug=True)
