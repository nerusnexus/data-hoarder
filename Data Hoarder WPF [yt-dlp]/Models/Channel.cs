using System;

namespace DataHoarder.Models
{
    public class Channel
    {
        public string Id { get; set; } // TEXT PRIMARY KEY
        public string GroupName { get; set; }
        public string FolderName { get; set; }
        public string Url { get; set; }
        public string AvatarPath { get; set; }
        public string ConfigJson { get; set; }
        public string StatsJson { get; set; }
        public string LastChecked { get; set; }
        public string CreatedAt { get; set; }
    }
}