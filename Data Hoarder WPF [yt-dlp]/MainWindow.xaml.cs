using System;
using System.Windows;
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
                RootNavigation.SetPageService(new PageService());
                RootNavigation.Navigate(typeof(DashboardPage));
            };
        }
    }

    public class PageService : Wpf.Ui.IPageService
    {
        public T? GetPage<T>() where T : class => (T?)Activator.CreateInstance(typeof(T));
        public FrameworkElement? GetPage(Type pageType) => Activator.CreateInstance(pageType) as FrameworkElement;
    }
}