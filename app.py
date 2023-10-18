from src.main import MainApplication
from src.utility import create_csv


def main():
    create_csv()
    app = MainApplication(None)
    app.mainloop()


if __name__ == "__main__":
    main()
