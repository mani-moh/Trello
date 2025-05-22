import sqlite3
def init_db():
    conn = sqlite3.connect('trello.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    username INTEGER UNIQUE NOT NULL CHECK(username BETWEEN 1000 AND 9999)
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS project_users (
                    project_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    PRIMARY KEY (project_id, user_id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS subboards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subboard_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    FOREIGN KEY(subboard_id) REFERENCES subboards(id) ON DELETE CASCADE
                    )''')

    conn.commit()
    conn.close()