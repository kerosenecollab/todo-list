import sqlite3
from sqlite3 import Error

def create_connection():
    """Создать соединение с базой данных SQLite"""
    conn = None
    try:
        conn = sqlite3.connect('todo.db')
        return conn
    except Error as e:
        print(e)
    
    return conn

def create_table(conn):
    """Создать таблицу задач, если она не существует"""
    try:
        sql = '''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    is_completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );'''
        cursor = conn.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)

def init_db():
    """Инициализировать базу данных"""
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()

# CRUD операции
def add_task(conn, title, description=""):
    """Добавить новую задачу"""
    sql = '''INSERT INTO tasks(title, description) VALUES(?,?)'''
    cursor = conn.cursor()
    cursor.execute(sql, (title, description))
    conn.commit()
    return cursor.lastrowid

def get_all_tasks(conn):
    """Получить все задачи"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    return cursor.fetchall()

def get_task_by_id(conn, task_id):
    """Получить задачу по ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    return cursor.fetchone()

def update_task(conn, task_id, title, description, is_completed):
    """Обновить задачу"""
    sql = '''UPDATE tasks 
              SET title = ?, description = ?, is_completed = ?
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (title, description, is_completed, task_id))
    conn.commit()

def delete_task(conn, task_id):
    """Удалить задачу"""
    sql = 'DELETE FROM tasks WHERE id=?'
    cursor = conn.cursor()
    cursor.execute(sql, (task_id,))
    conn.commit()
