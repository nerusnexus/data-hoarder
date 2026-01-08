# core/manager.py
import os
import sqlite3
import shutil

class DataManager:
    def __init__(self):
        self.root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Root Test")
        os.makedirs(self.root_path, exist_ok=True)
        self.db_path = "data_hoarder.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER,
                    name TEXT,
                    url TEXT,
                    FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
                )
            """)

    def add_group(self, name):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO groups (name) VALUES (?)", (name,))
            os.makedirs(os.path.join(self.root_path, name), exist_ok=True)
            return True
        except: return False

    def delete_item(self, name, is_group, parent_group=None):
        with sqlite3.connect(self.db_path) as conn:
            if is_group:
                conn.execute("DELETE FROM groups WHERE name=?", (name,))
                path = os.path.join(self.root_path, name)
            else:
                conn.execute("DELETE FROM channels WHERE name=?", (name,))
                path = os.path.join(self.root_path, parent_group, name)

            if os.path.exists(path):
                shutil.rmtree(path)

    def rename_item(self, old_name, new_name, is_group, parent_group=None):
        with sqlite3.connect(self.db_path) as conn:
            if is_group:
                conn.execute("UPDATE groups SET name=? WHERE name=?", (new_name, old_name))
                old_path = os.path.join(self.root_path, old_name)
                new_path = os.path.join(self.root_path, new_name)
            else:
                conn.execute("UPDATE channels SET name=? WHERE name=?", (new_name, old_name))
                old_path = os.path.join(self.root_path, parent_group, old_name)
                new_path = os.path.join(self.root_path, parent_group, new_name)

            if os.path.exists(old_path):
                os.rename(old_path, new_path)
