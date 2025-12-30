using System;

namespace DataHoarder.Models
{
    public class Video
    {
        public string Id { get; set; } // TEXT PRIMARY KEY
        public string ChannelId { get; set; }
        public string Title { get; set; }
        public string UploadDate { get; set; }
        public long Duration { get; set; }
        public long ViewCount { get; set; }
        public long LikeCount { get; set; }
        public long CommentCount { get; set; }
        public string Resolution { get; set; }
        public int Fps { get; set; }
        public string Status { get; set; } // 'Downloaded', 'Missing', etc.
        public string OnlineStatus { get; set; } // 'Online', 'Deleted', etc.
        public string LastUpdated { get; set; }
        public string VideoFileDate { get; set; }
        public string VideoType { get; set; } // 'Video', 'Live'
        public string FilePath { get; set; }
        public string Description { get; set; }
        public string Tags { get; set; }
        public string MetadataJson { get; set; }
    }
}