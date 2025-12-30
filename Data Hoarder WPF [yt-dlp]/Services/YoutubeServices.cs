using System;
using System.IO;
using System.Threading.Tasks;
using YoutubeDLSharp;
using YoutubeDLSharp.Options;

namespace DataHoarder.Services
{
    public class YoutubeEngine
    {
        private readonly YoutubeDL _ytdl;
        private readonly string _binariesPath;

        public YoutubeEngine()
        {
            var appRoot = AppDomain.CurrentDomain.BaseDirectory;
            _binariesPath = Path.Combine(appRoot, "Binaries");

            if (!Directory.Exists(_binariesPath))
                Directory.CreateDirectory(_binariesPath);

            _ytdl = new YoutubeDL();
            _ytdl.YoutubeDLPath = Path.Combine(_binariesPath, "yt-dlp.exe");
            _ytdl.FFmpegPath = Path.Combine(_binariesPath, "ffmpeg.exe");
        }

        public async Task InitializeAsync(IProgress<string> progress)
        {
            progress?.Report("Checking binaries...");
            if (!File.Exists(_ytdl.YoutubeDLPath)) await Utils.DownloadYtDlp(_binariesPath);
            if (!File.Exists(_ytdl.FFmpegPath)) await Utils.DownloadFFmpeg(_binariesPath);
            progress?.Report("Engine Ready.");
        }

        public async Task<RunResult<string>> DownloadVideoAsync(string url, string outputFolder, IProgress<DownloadProgress> progress)
        {
            var options = new OptionSet()
            {
                Output = Path.Combine(outputFolder, "%(title)s [%(id)s].%(ext)s"),
                RestrictFilenames = true,
                Overwrite = false,
                Format = "bestvideo+bestaudio/best",
                MergeOutputFormat = DownloadMergeFormat.Mp4,
            };

            return await _ytdl.RunVideoDownload(url, progress: progress, overrideOptions: options);
        }
    }
}