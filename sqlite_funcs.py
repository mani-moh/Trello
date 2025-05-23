import random
import sqlite3

def init_db():
    conn = sqlite3.connect('trello.sqlite')
    cursor = conn.cursor()



    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    username INTEGER UNIQUE NOT NULL CHECK(username BETWEEN 1000 AND 9999),
                    is_admin BOOLEAN DEFAULT FALSE,
                    phone_number TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        leader_id INTEGER UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (leader_id) REFERENCES users(id)
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS project_members (
                            project_id INTEGER NOT NULL,
                            user_id INTEGER NOT NULL,
                            PRIMARY KEY (project_id, user_id),
                            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
                    deadline TIMESTAMP,
                    priority INTEGER CHECK(priority IN (1,2,3,4,5)),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(subboard_id) REFERENCES subboards(id) ON DELETE CASCADE
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS task_members (
                        task_id INTEGER NOT NULL ,
                        user_id INTEGER NOT NULL,
                        PRIMARY KEY (task_id, user_id),
                        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ActivityLog (
                        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        action_type TEXT NOT NULL,
                        entity_type TEXT NOT NULL,  -- 'User', 'Project', 'Task'
                        entity_id INTEGER,
                        details TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        )''')



    conn.commit()
    conn.close()

def login_check(username, password):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return True
    else:
        return False

def signup_check(firstname, lastname, password, email):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    email = cursor.fetchone()
    conn.close()

    if email:
        return False
    else:
        return True

def signup_register(firstname, lastname, password, email):
    conn = None
    username = random_username("trello.sqlite")
    try:
        conn = sqlite3.connect("trello.sqlite")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (type, first_name, last_name, email, password, username) VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, firstname, lastname, email, password, username))



        conn.commit()
        return username

    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn:
            conn.close()
def random_username(db:str):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    num = random.randint(1000, 9999)
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (num,))
    username_exists = cursor.fetchone()
    conn.close()

    if username_exists:
        return random_username(db)
    else:
        return num