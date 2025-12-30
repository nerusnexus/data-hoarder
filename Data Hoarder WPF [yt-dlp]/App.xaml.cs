using System.Windows;
using DataHoarder.Services;

namespace DataHoarder
{
    public partial class App : Application
    {
        public YoutubeEngine Engine { get; private set; } = default!;
        public DatabaseService Database { get; private set; } = default!;

        protected override async void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            // Define o caminho do banco de dados
            string root = System.IO.Path.Combine(System.Environment.GetFolderPath(System.Environment.SpecialFolder.MyDocuments), "YTDlpHoarder_Root");

            Database = new DatabaseService(root);
            Engine = new YoutubeEngine();

            var mainWindow = new MainWindow();
            mainWindow.Show();

            await Engine.InitializeAsync(null!);
        }
    }
}