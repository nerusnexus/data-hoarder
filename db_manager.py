# core/manager.py
import os
import sqlite3
import shutil
import json

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
            # Expanded table to store yt-dlp data
            conn.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER,
                    name TEXT,
                    url TEXT,
                    channel_id TEXT,
                    uploader TEXT,
                    subscribers INTEGER,
                    description TEXT,
                    thumbnail TEXT,
                    raw_data TEXT,
                    FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
                )
            """)

    def add_group(self, name):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO groups (name) VALUES (?)", (name,))
            os.makedirs(os.path.join(self.root_path, name), exist_ok=True)
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding group: {e}")
            return False

    def add_channel(self, group_name, channel_data):
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get Group ID
                cursor = conn.execute("SELECT id FROM groups WHERE name=?", (group_name,))
                group_row = cursor.fetchone()
                if not group_row:
                    return False
                group_id = group_row[0]

                # Extract data safely
                name = channel_data.get('title', channel_data.get('channel', 'Unknown'))
                url = channel_data.get('webpage_url', channel_data.get('original_url', ''))
                c_id = channel_data.get('channel_id', '')
                uploader = channel_data.get('uploader', '')
                subs = channel_data.get('subscriber_count', 0)
                desc = channel_data.get('description', '')
                thumb = channel_data.get('thumbnails', [{}])[-1].get('url', '') if channel_data.get('thumbnails') else ''

                # Save full raw data just in case
                raw = json.dumps(channel_data)

                conn.execute("""
                    INSERT INTO channels (group_id, name, url, channel_id, uploader, subscribers, description, thumbnail, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (group_id, name, url, c_id, uploader, subs, desc, thumb, raw))

            # Create folder structure
            # Sanitize name for folder creation
            safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
            os.makedirs(os.path.join(self.root_path, group_name, safe_name), exist_ok=True)
            return True
        except Exception as e:
            print(f"Error adding channel: {e}")
            return False

    def delete_item(self, name, is_group, parent_group=None):
        with sqlite3.connect(self.db_path) as conn:
            if is_group:
                conn.execute("DELETE FROM groups WHERE name=?", (name,))
                path = os.path.join(self.root_path, name)
            else:
                conn.execute("DELETE FROM channels WHERE name=? AND group_id=(SELECT id FROM groups WHERE name=?)", (name, parent_group))
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
                # Find group id first to be precise
                cursor = conn.execute("SELECT id FROM groups WHERE name=?", (parent_group,))
                group_id = cursor.fetchone()[0]
                conn.execute("UPDATE channels SET name=? WHERE name=? AND group_id=?", (new_name, old_name, group_id))
                old_path = os.path.join(self.root_path, parent_group, old_name)
                new_path = os.path.join(self.root_path, parent_group, new_name)

            if os.path.exists(old_path):
                os.rename(old_path, new_path)

    def get_groups(self):
        with sqlite3.connect(self.db_path) as conn:
            return [row[0] for row in conn.execute("SELECT name FROM groups")]

    def get_channels(self, group_name):
        with sqlite3.connect(self.db_path) as conn:
            return [row[0] for row in conn.execute(
                "SELECT name FROM channels WHERE group_id=(SELECT id FROM groups WHERE name=?)",
                (group_name,))]
