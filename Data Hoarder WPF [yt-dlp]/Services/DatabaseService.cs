using Dapper;
using DataHoarder.Models;
using Microsoft.Data.Sqlite;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using DataHoarder.Models;

namespace DataHoarder.Services
{
    public class DatabaseService
    {
        private string _dbPath;
        private string _connectionString;

        public DatabaseService(string rootPath)
        {
            // Define o caminho igual ao do Python: Root/Config/library.db
            string configDir = Path.Combine(rootPath, "Config");
            if (!Directory.Exists(configDir)) Directory.CreateDirectory(configDir);

            _dbPath = Path.Combine(configDir, "library.db");
            _connectionString = $"Data Source={_dbPath}";

            InitializeDatabase();
        }

        private void InitializeDatabase()
        {
            using (var conn = new SqliteConnection(_connectionString))
            {
                conn.Open();

                // Recriando a tabela Channels
                conn.Execute(@"CREATE TABLE IF NOT EXISTS channels (
                    id TEXT PRIMARY KEY,
                    group_name TEXT,
                    folder_name TEXT,
                    url TEXT,
                    avatar_path TEXT,
                    config_json TEXT,
                    stats_json TEXT,
                    last_checked TEXT,
                    created_at TEXT
                )");

                // Recriando a tabela Videos
                conn.Execute(@"CREATE TABLE IF NOT EXISTS videos (
                    id TEXT PRIMARY KEY,
                    channel_id TEXT,
                    title TEXT,
                    upload_date TEXT,
                    duration INTEGER,
                    view_count INTEGER,
                    like_count INTEGER,
                    comment_count INTEGER,
                    resolution TEXT,
                    fps INTEGER,
                    status TEXT,
                    online_status TEXT DEFAULT 'Unknown',
                    last_updated TEXT,
                    video_file_date TEXT,
                    video_type TEXT,
                    file_path TEXT,
                    description TEXT,
                    tags TEXT,
                    metadata_json TEXT,
                    FOREIGN KEY(channel_id) REFERENCES channels(id) ON DELETE CASCADE
                )");

                // Índices
                conn.Execute("CREATE INDEX IF NOT EXISTS idx_videos_channel ON videos(channel_id)");
                conn.Execute("CREATE INDEX IF NOT EXISTS idx_videos_date ON videos(upload_date)");
            }
        }

        // --- Métodos de CRUD (Exemplos convertidos do Python) ---

        public async Task UpsertChannelAsync(Channel channel)
        {
            using (var conn = new SqliteConnection(_connectionString))
            {
                var sql = @"
                    INSERT INTO channels (id, group_name, folder_name, url, avatar_path, config_json, created_at)
                    VALUES (@Id, @GroupName, @FolderName, @Url, @AvatarPath, @ConfigJson, datetime('now'))
                    ON CONFLICT(id) DO UPDATE SET
                        group_name=excluded.group_name,
                        folder_name=excluded.folder_name,
                        url=COALESCE(excluded.url, url),
                        avatar_path=COALESCE(excluded.avatar_path, avatar_path),
                        config_json=COALESCE(excluded.config_json, config_json)";

                await conn.ExecuteAsync(sql, channel);
            }
        }

        public async Task<IEnumerable<Channel>> GetAllChannelsAsync()
        {
            using (var conn = new SqliteConnection(_connectionString))
            {
                return await conn.QueryAsync<Channel>("SELECT * FROM channels ORDER BY group_name, folder_name");
            }
        }

        public async Task UpsertVideoAsync(Video video)
        {
            // Validação simples igual ao Python
            if (video.Id.Length > 15 && (video.Id.StartsWith("UC") || video.Id.StartsWith("PL"))) return;

            using (var conn = new SqliteConnection(_connectionString))
            {
                var sql = @"
                    INSERT INTO videos (
                        id, channel_id, title, upload_date, duration, 
                        view_count, like_count, comment_count, 
                        resolution, fps, status, online_status, 
                        last_updated, video_file_date,
                        video_type, file_path, tags
                    ) VALUES (
                        @Id, @ChannelId, @Title, @UploadDate, @Duration, 
                        @ViewCount, @LikeCount, @CommentCount, 
                        @Resolution, @Fps, @Status, @OnlineStatus, 
                        @LastUpdated, @VideoFileDate,
                        @VideoType, @FilePath, @Tags
                    )
                    ON CONFLICT(id) DO UPDATE SET
                        title=excluded.title,
                        view_count=excluded.view_count,
                        resolution=COALESCE(excluded.resolution, resolution),
                        fps=COALESCE(excluded.fps, fps),
                        status=excluded.status,
                        online_status=COALESCE(excluded.online_status, online_status),
                        last_updated=excluded.last_updated,
                        video_file_date=COALESCE(excluded.video_file_date, video_file_date),
                        file_path=COALESCE(excluded.file_path, file_path)";

                await conn.ExecuteAsync(sql, video);
            }
        }
    }
}