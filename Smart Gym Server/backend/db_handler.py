import sqlite3
import os

class DBHandler:
    DEFAULT_DB_FILE = "smartgym.db"

    def __init__(self, db_name=DEFAULT_DB_FILE):
        self.db_name = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name))
        if not os.path.exists(os.path.dirname(self.db_name)):
            os.makedirs(os.path.dirname(self.db_name))
        self.init_db()

    def init_db(self):
        conn = self.get_conn()
        cur = conn.cursor()
        schema_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
        with open(schema_file, 'r') as f:
            cur.executescript(f.read())
        conn.commit()
        conn.close()

    def get_conn(self):
        return sqlite3.connect(self.db_name, timeout=100)

    def add_user(self, uuid, name, signup_date):
        conn = self.get_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (uuid, name, signup_date) VALUES (?, ?, ?)", (uuid, name, signup_date))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        conn.close()

    def add_machine(self, name, description):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO machines (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        conn.close()

    def add_workout(self, user_id, machine_id, date, repetitions, weight, duration):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO workouts (user_id, machine_id, date, repetitions weight, duration) VALUES (?, ?, ?, ?, ?, ?)", (user_id, machine_id, date, repetitions, weight, duration))
        conn.commit()
        conn.close()

    def get_users(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_machines(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM machines")
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_workouts(self):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM workouts")
        rows = cur.fetchall()
        conn.close()
        return rows

    def delete_user(self, user_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

    def delete_machine(self, machine_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM machines WHERE id = ?", (machine_id,))
        conn.commit()
        conn.close()

    def delete_workout(self, workout_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
        conn.commit()
        conn.close()

    def get_user_by_id(self, user_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return row

    def get_machine_by_id(self, machine_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM machines WHERE id = ?", (machine_id,))
        row = cur.fetchone()
        conn.close()
        return row

    def get_workout_by_id(self, workout_id):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,))
        row = cur.fetchone()
        conn.close()
        return row

    def get_user_by_uuid(self, uuid):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE uuid = ?", (uuid,))
        row = cur.fetchone()
        conn.close()
        return row
    
    def get_user_by_name(self, name):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name = ?", (name,))
        row = cur.fetchone()
        conn.close()
        return row

    def check_user_by_name(self, name):
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE name = ?", (name,))
        exists = cur.fetchone() is not None
        conn.close()
        return exists
    
    def get_workouts_by_user(self, user):
        user_id = self.get_user_by_name(user)[0]
        
        conn = self.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM workouts WHERE user_id = ?", (user_id,))
        rows = cur.fetchall()
        conn.close()
        return rows
