# core/manager.py
import os
import sqlite3
import shutil
import json
import urllib.request
from config_manager import ConfigManager

class DataManager:
    def __init__(self):
        # Use the Root path defined in Settings
        self.root_path = ConfigManager.get_root_path()
        os.makedirs(self.root_path, exist_ok=True)

        # Store DB in the root path
        self.db_path = os.path.join(self.root_path, "data_hoarder.db")
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON;") # Enable FK support

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
                    channel_id TEXT,
                    uploader TEXT,
                    subscribers INTEGER,
                    description TEXT,
                    thumbnail TEXT,
                    raw_data TEXT,
                    FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
                )
            """)

            # --- NOVA TABELA DE VÍDEOS ---
            conn.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_db_id INTEGER,
                    video_id TEXT,
                    title TEXT,
                    url TEXT,
                    duration REAL,
                    view_count INTEGER,
                    thumbnail TEXT,
                    upload_date TEXT,
                    FOREIGN KEY(channel_db_id) REFERENCES channels(id) ON DELETE CASCADE
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
                # 1. Get Group ID
                cursor = conn.execute("SELECT id FROM groups WHERE name=?", (group_name,))
                group_row = cursor.fetchone()
                if not group_row:
                    return False
                group_id = group_row[0]

                # 2. Extract Channel Data
                name = channel_data.get('title', channel_data.get('channel', 'Unknown'))
                url = channel_data.get('webpage_url', channel_data.get('original_url', ''))
                c_id = channel_data.get('channel_id', '')
                uploader = channel_data.get('uploader', '')

                # Tenta pegar inscritos de várias chaves possíveis
                subs = channel_data.get('subscriber_count')
                if subs is None:
                    subs = channel_data.get('channel_follower_count', 0)

                desc = channel_data.get('description', '')

                # Pega a melhor thumbnail disponível do canal
                thumb = ''
                if channel_data.get('thumbnails'):
                    thumb = channel_data['thumbnails'][-1].get('url', '')

                # Salva o JSON bruto
                raw = json.dumps(channel_data)

                # 3. Insert Channel
                cursor = conn.execute("""
                    INSERT INTO channels (group_id, name, url, channel_id, uploader, subscribers, description, thumbnail, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (group_id, name, url, c_id, uploader, subs, desc, thumb, raw))

                channel_db_id = cursor.lastrowid # ID do canal recém criado no banco

                # 4. PROCESS VIDEOS (ENTRIES)
                entries = channel_data.get('entries', [])
                if entries:
                    video_rows = []
                    for entry in entries:
                        # Só processa se for um video/url válido
                        if entry.get('_type') == 'url' or entry.get('ie_key') == 'Youtube':
                            v_id = entry.get('id', '')
                            v_title = entry.get('title', 'Unknown')
                            v_url = entry.get('url', '')
                            v_duration = entry.get('duration', 0)
                            v_views = entry.get('view_count', 0)
                            v_date = entry.get('upload_date', '') # Formato YYYYMMDD se disponível

                            # Tenta pegar thumbnail do vídeo (que fica dentro da entry)
                            v_thumb = ''
                            if entry.get('thumbnails'):
                                v_thumb = entry['thumbnails'][-1].get('url', '')

                            video_rows.append((channel_db_id, v_id, v_title, v_url, v_duration, v_views, v_thumb, v_date))

                    if video_rows:
                        conn.executemany("""
                            INSERT INTO videos (channel_db_id, video_id, title, url, duration, view_count, thumbnail, upload_date)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, video_rows)

            # --- File System Operations ---

            # Create Folder Structure: Root/Group/@Channel
            # Sanitize name
            safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
            folder_name = f"@{safe_name}"
            channel_path = os.path.join(self.root_path, group_name, folder_name)
            os.makedirs(channel_path, exist_ok=True)

            # Save metadata.json
            with open(os.path.join(channel_path, "metadata.json"), "w", encoding='utf-8') as f:
                json.dump(channel_data, f, indent=4, ensure_ascii=False)

            # Download Assets (Banner and PFP)
            self._download_assets(channel_data, channel_path, thumb)

            return True
        except Exception as e:
            print(f"Error adding channel: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _download_assets(self, data, path, thumb_url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        # Download Profile Picture
        if thumb_url:
            try:
                ext = ".jpg"
                if ".png" in thumb_url: ext = ".png"
                elif ".webp" in thumb_url: ext = ".webp"
                urllib.request.urlretrieve(thumb_url, os.path.join(path, f"profile_picture{ext}"))
            except Exception as e:
                print(f"Failed to download PFP: {e}")

        # Download Banner
        banners = data.get('banners', [])
        if banners:
            banner_url = banners[-1].get('url')
            if banner_url:
                try:
                    ext = ".jpg"
                    if ".png" in banner_url: ext = ".png"
                    elif ".webp" in banner_url: ext = ".webp"
                    urllib.request.urlretrieve(banner_url, os.path.join(path, f"banner{ext}"))
                except Exception as e:
                    print(f"Failed to download Banner: {e}")

    def delete_item(self, name, is_group, parent_group=None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            if is_group:
                conn.execute("DELETE FROM groups WHERE name=?", (name,))
                path = os.path.join(self.root_path, name)
            else:
                conn.execute("DELETE FROM channels WHERE name=? AND group_id=(SELECT id FROM groups WHERE name=?)", (name, parent_group))

                safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
                path = os.path.join(self.root_path, parent_group, f"@{safe_name}")
                if not os.path.exists(path):
                    path = os.path.join(self.root_path, parent_group, safe_name)

            if os.path.exists(path):
                shutil.rmtree(path)

    def rename_item(self, old_name, new_name, is_group, parent_group=None):
        with sqlite3.connect(self.db_path) as conn:
            if is_group:
                conn.execute("UPDATE groups SET name=? WHERE name=?", (new_name, old_name))
                old_path = os.path.join(self.root_path, old_name)
                new_path = os.path.join(self.root_path, new_name)
            else:
                cursor = conn.execute("SELECT id FROM groups WHERE name=?", (parent_group,))
                group_id = cursor.fetchone()[0]
                conn.execute("UPDATE channels SET name=? WHERE name=? AND group_id=?", (new_name, old_name, group_id))

                old_safe = "".join([c for c in old_name if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
                new_safe = "".join([c for c in new_name if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()

                old_path = os.path.join(self.root_path, parent_group, f"@{old_safe}")
                new_path = os.path.join(self.root_path, parent_group, f"@{new_safe}")

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
