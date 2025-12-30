using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using DataHoarder.Models;
using DataHoarder.Services;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using System.Windows;

namespace DataHoarder.ViewModels
{
    public partial class DashboardViewModel : ObservableObject
    {
        private readonly DatabaseService _databaseService = null!;

        [ObservableProperty]
        private ObservableCollection<Channel> _channels;

        [ObservableProperty]
        private bool _isLoading;

        public DashboardViewModel()
        {
            if (Application.Current is App app)
                _databaseService = app.Database;

            Channels = new ObservableCollection<Channel>();
            _ = LoadChannels();
        }

        [RelayCommand]
        public async Task LoadChannels()
        {
            if (_databaseService == null) return;
            IsLoading = true;
            Channels.Clear();
            var data = await _databaseService.GetAllChannelsAsync();
            foreach (var item in data) Channels.Add(item);
            IsLoading = false;
        }
    }
}