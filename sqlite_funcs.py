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
                        leader_id INTEGER NOT NULL,
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

def signup_check(email):
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


def get_userid_with_username(username):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
                SELECT id FROM users WHERE username = ?
            ''', (username,))
    row = cursor.fetchone()
    user_id = row[0]
    conn.close()
    return user_id

def get_username_with_userid(userid):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
                SELECT username FROM users WHERE id = ?
            ''', (userid,))
    row = cursor.fetchone()
    username = row[0]
    conn.close()
    return username

def get_projects_by_username(username):
    user_id = get_userid_with_username(username)
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    projects = {
        "admin": [],
        "leader": [],
        "member": []
    }






    #return all project ids if username is admin
    cursor.execute('''
        SELECT 1 FROM users WHERE is_admin =1 AND username = ?
    ''', (username,))
    admin = cursor.fetchone()
    if admin:
        cursor.execute('''
            SELECT * FROM projects
        ''')
        all_projects = cursor.fetchall()
        projects["admin"] = [project[0] for project in all_projects]


    # return all project ids if username is leader
    cursor.execute('''
        SELECT * FROM projects WHERE leader_id = ?
    ''', (user_id,))

    leader_projects = cursor.fetchall()
    projects["leader"] = [project[0] for project in leader_projects]

    # return all project ids if username is member
    cursor.execute('''
        SELECT * FROM project_members WHERE user_id = ?
    ''', (user_id,))

    member_projects = cursor.fetchall()
    projects["member"] = [project[0] for project in member_projects]


    conn.close()
    return projects

# self.user_data = {
#             "first name": "",
#             "last name": "",
#             "email": "",
#             "type": "",
#             "is admin": False,
#             "phone number": ""
#         }

def get_user_data(username):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''',(username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "first name": row[1],
            "last name": row[2],
            "email": row[4],
            "type": row[5],
            "is admin": row[7],
            "phone number": row[8],
            "date created": row[9],
        }

def username_exists(username):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return True
    else:
        return False

def project_register(name: str, usernames: list, user_id: int):


    conn = None
    try:
        conn = sqlite3.connect("trello.sqlite")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO projects (name, leader_id) VALUES (?, ?)
        ''',(name,user_id))

        project_id = cursor.lastrowid


        for username in usernames:
            member_id = get_userid_with_username(username)
            cursor.execute('''
                        INSERT INTO project_members (project_id, user_id) VALUES (?, ?)
                    ''', (project_id, member_id))

        conn.commit()
        return project_id



    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn:
            conn.close()


def get_project_data_with_id(project_id):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
            SELECT * FROM projects WHERE id = ?
        ''', (project_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        leader_data = get_user_data(get_username_with_userid(row[2]))
        return {
            "name": row[1],
            "leader": row[2],
            "date created": row[3],
            "first name": leader_data["first name"],
            "last name": leader_data["last name"],
        }



def delete_project(project_id):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM projects WHERE id = ?
    ''',(project_id,))
    cursor.execute('''
            DELETE FROM project_members WHERE project_id = ?
        ''', (project_id,))
    conn.commit()
    conn.close()


def get_task_basic_info_by_project_id(project_id, order_by):
    task_ids = {}
    subboard_name = {}



    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name FROM subboards WHERE project_id = ?
    ''',(project_id,))

    rows = cursor.fetchall()
    for row in rows:
        try:
            subboard_id = row[0]
            subboard_name[subboard_id] = row[1]
            task_ids[subboard_id] = []
            cursor.execute(f'''
                    SELECT id, name, priority, created_at FROM tasks WHERE subboard_id = ? ORDER BY {order_by}  
                ''', (subboard_id,))
            s_rows = cursor.fetchall()
            for s_row in s_rows:
                task_info = {
                    "id": s_row[0],
                    "name": s_row[1],
                    "priority": s_row[2],
                    "created_at": s_row[3],
                }
                task_ids[subboard_id].append(task_info)

        except IndexError:
            pass


    info = {
        "subboard_name": subboard_name,
        "task_ids": task_ids,
    }
    return info

def delete_card(card_id):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM tasks WHERE id = ?
    ''',(card_id,))
    cursor.execute('''
            DELETE FROM task_members WHERE task_id = ?
        ''', (card_id,))
    conn.commit()
    conn.close()

def get_card_data(card_id):
    data = {}
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tasks WHERE id = ?
    ''',(card_id,))
    row1 = cursor.fetchone()

    cursor.execute('''
            SELECT user_id FROM task_members WHERE task_id = ?
        ''', (card_id,))
    rows = cursor.fetchall()
    member_ids = [r[0] for r in rows]
    members = {}
    for member_id in member_ids:
        cursor.execute('''
                    SELECT username, first_name, last_name FROM users WHERE id = ?
                ''', (member_id,))
        m_row = cursor.fetchone()
        members[member_id] = list(m_row)
    conn.close()

    print(row1)
    # try:
    data["card_id"] = row1[0]
    data["subboard_id"] = row1[1]
    data["name"] = row1[2]
    data["description"] = row1[3]
    data["deadline"] = row1[4]
    data["priority"] = row1[5]
    data["created_at"] = row1[6]
    data["members"] = members


    # except IndexError:
    #     print(f"Index Error: {card_id}")
    #     pass
    print()
    return data

def get_subboard_name_by_id(subboard_id):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name FROM subboards WHERE id = ?
    ''',subboard_id)
    row = cursor.fetchone()
    conn.close()
    return row[0]


def change_name(card_id, new_name):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks SET name = ? WHERE id = ?
    ''',(new_name, card_id))
    conn.commit()
    conn.close()

def change_description(card_id, new_description):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks SET description = ? WHERE id = ?
    ''',(new_description, card_id))
    conn.commit()
    conn.close()

def change_deadline(card_id, deadline):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
            UPDATE tasks SET deadline = ? WHERE id = ?
        ''', (deadline, card_id))
    conn.commit()
    conn.close()

def change_priority(card_id, priority):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
                UPDATE tasks SET priority = ? WHERE id = ?
            ''', (priority, card_id))
    conn.commit()
    conn.close()

def change_subboard(card_id, sid):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
                UPDATE tasks SET subboard_id = ? WHERE id = ?
            ''', (sid, card_id))
    conn.commit()
    conn.close()

def add_task_members(card_id, usernames):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    for username in usernames:
        userid = get_userid_with_username(username)
        cursor.execute('''
            INSERT INTO task_members (task_id, user_id) VALUES (?, ?) 
        ''',(card_id, userid))
    conn.commit()
    conn.close()

def create_card(sid, name, description, deadline, priority, usernames):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (subboard_id, name, description, deadline, priority) VALUES (?, ?, ?, ?, ?)
    ''',(sid, name, description, deadline, priority))
    card_id = cursor.lastrowid
    for username in usernames:
        userid = get_userid_with_username(username)
        cursor.execute('''
        INSERT INTO task_members (task_id, user_id) VALUES (?, ?)
        ''',(card_id, userid))
    conn.commit()
    conn.close()

def create_subboard(name, project_id):
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO subboards (project_id, name) VALUES (?, ?)
    ''',(project_id, name))

    conn.commit()
    conn.close()

def has_access(username, card_id):
    userid = get_userid_with_username(username)
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM task_members WHERE task_id = ? AND user_id = ?
    ''',(card_id,userid))
    
    row1 = cursor.fetchone()

    cursor.execute('''
        SELECT * FROM users WHERE is_admin = TRUE AND id = ?
        ''', (userid,))
    row2 = cursor.fetchone()

    cursor.execute('''
            SELECT subboard_id FROM tasks WHERE  id = ?
            ''', (card_id,))
    sid = cursor.fetchone()[0]

    cursor.execute('''
            SELECT project_id FROM subboards WHERE id = ?
            ''', (sid,))
    pid = cursor.fetchone()[0]

    cursor.execute('''
            SELECT * FROM projects WHERE leader_id = ? AND id = ?
            ''', (userid, pid))
    row3 = cursor.fetchone()

    if row1 is not None or row2 is not None or row3 is not None:
        return True
    else:
        return False






def test_get():
    conn = sqlite3.connect("trello.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchone())

