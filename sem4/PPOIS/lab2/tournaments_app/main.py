from controller import TournamentController
from view import MainWindow

def main():
    app_controller = TournamentController()
    app_view = MainWindow(app_controller)
    app_controller.set_view(app_view)
    
    app_controller.run()

if __name__ == "__main__":
    main()