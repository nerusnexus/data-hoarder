using System;
using System.Windows;
using Wpf.Ui;
using Wpf.Ui.Abstractions; // Required for INavigationViewPageProvider
using Wpf.Ui.Controls;
using DataHoarder.Views;

namespace DataHoarder
{
    public partial class MainWindow : FluentWindow
    {
        public MainWindow()
        {
            InitializeComponent();
            Loaded += (s, e) =>
            {
                // ERROR FIX: Use 'SetPageProviderService' instead of 'SetPageService'
                RootNavigation.SetPageProviderService(new PageService());
                RootNavigation.Navigate(typeof(DashboardPage));
            };
        }
    }

    // ERROR FIX: Implement 'INavigationViewPageProvider' instead of 'IPageService'
    public class PageService : INavigationViewPageProvider
    {
        // This method is required by the interface
        public object? GetPage(Type pageType)
        {
            return Activator.CreateInstance(pageType);
        }
    }
}