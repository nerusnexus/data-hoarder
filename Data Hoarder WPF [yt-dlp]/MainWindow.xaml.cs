using DataHoarder.Views;
using System;
using System.Windows;
using Wpf.Ui.Controls; // Namespace do WPF-UI
using DataHoarder.Views;

namespace DataHoarder
{
    // A classe deve herdar de FluentWindow, não Window
    public partial class MainWindow : FluentWindow
    {
        public MainWindow()
        {
            InitializeComponent();
            Loaded += OnLoaded;
        }

        private void OnLoaded(object sender, RoutedEventArgs e)
        {
            // Vincula o Frame ao NavigationView
            RootNavigation.SetPageService(new PageService());
            // Navega para a primeira página ao iniciar
            RootNavigation.Navigate(typeof(DashboardPage));
        }
    }

    // Serviço simples para instanciar as páginas (necessário para o WPF-UI simples)
    public class PageService : Wpf.Ui.IPageService
    {
        public T? GetPage<T>() where T : class
        {
            if (!typeof(FrameworkElement).IsAssignableFrom(typeof(T)))
                throw new InvalidOperationException("The page should be a WPF control.");

            return (T?)Activator.CreateInstance(typeof(T));
        }

        public FrameworkElement? GetPage(Type pageType)
        {
            if (!typeof(FrameworkElement).IsAssignableFrom(pageType))
                throw new InvalidOperationException("The page should be a WPF control.");

            return Activator.CreateInstance(pageType) as FrameworkElement;
        }
    }
}