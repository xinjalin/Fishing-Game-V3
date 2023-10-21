import tkinter as tk
from src.utility import *
from src.fishing_game import *


class LoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Login")

        # GUI components for Login Window
        self.username_label = tk.Label(self, text="Username")
        self.password_label = tk.Label(self, text="Password")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")  # Show asterisks for password input
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.home_button = tk.Button(self, text="Home", command=self.home)

        # Position GUI components on the Login Window
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.login_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="w")
        self.home_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="e")

    def login(self):
        # login logic here
        username = self.entry_username.get()
        password = self.entry_password.get()

        if is_present_in_csv(username):
            csv_user_data = get_password(username)
            is_match = check_password(password, csv_user_data)
            if is_match:
                self.withdraw()
                game_window = GameWindow(self)
                game_window.protocol("WM_DELETE_WINDOW", self.destroy_window)
            else:
                pass  # not is_match
        else:
            pass  # not present in csv

    def home(self):
        self.destroy()
        self.master.deiconify()

    def destroy_window(self):
        self.master.destroy()  # Close the application


class RegistrationWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Registration")

        # GUI components for Login Window
        self.username_label = tk.Label(self, text="Username")
        self.password_label = tk.Label(self, text="Password")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self)
        self.login_button = tk.Button(self, text="Register", command=self.register)
        self.home_button = tk.Button(self, text="Home", command=self.home)

        # Position GUI components on the Login Window
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.login_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="w")
        self.home_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="e")

    def register(self):
        # register logic here
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "" or password == "":
            print('username or password not supplied')
        else:
            if is_present_in_csv(username):  # user already exists
                print(f"username: {username} all ready exists")  # change to gui
            else:  # register user
                hpw = hash_password(password)
                data = {'username': username, 'password_hash': hpw}
                save_to_csv(data)

                self.destroy()
                self.master.deiconify()

    def home(self):
        self.destroy()
        self.master.deiconify()

    def destroy_window(self):
        self.master.destroy()  # Close the application


class GameWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Game")
        # Add widgets and logic for the game
        # GUI
        # button (gofish, keepfish, releasefish)
        # label (current fish)

        # logic
        # track record of catches
        # store the record of each cast of the fishing rod calculate the points for the player
        # delete record from record of catches if released

        fish = read_fish_csv()

        result_of_fishing = go_fishing(fish)
        print(result_of_fishing)

        # for fish_obj in fish:  # debug
        #     print(f'fish: {fish_obj}')


class MainApplication(tk.Tk):
    def __init__(self, master):
        super().__init__(master)
        self.title("Fishing Game")
        self.geometry("300x100")
        self.resizable(False, False)

        self.photo = tk.PhotoImage(file="assets/fish-304097_640.gif")

        # Restrict the size of the image (you can keep this part if you want)
        base_width = 100
        base_height = 60
        img_width = self.photo.width()
        img_height = self.photo.height()
        x_factor = img_width // base_width
        y_factor = img_height // base_height
        factor = max(x_factor, y_factor)
        if factor > 1:
            self.photo = self.photo.subsample(factor)

        # Display the image on the left
        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Frame to hold the buttons
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Pack the buttons inside the frame
        self.login_button = tk.Button(self.buttons_frame, text="Login", command=self.open_login_window)
        self.login_button.config(width=25, height=1)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self.buttons_frame, text="Register", command=self.open_registration_window)
        self.register_button.config(width=25, height=1)
        self.register_button.pack(pady=5)

    def open_login_window(self):
        self.withdraw()
        login_window = LoginWindow(self)
        login_window.protocol("WM_DELETE_WINDOW", self.destroy_main_window)  # Bind the close event to all windows

    def open_registration_window(self):
        self.withdraw()
        registration_window = RegistrationWindow(self)
        registration_window.protocol("WM_DELETE_WINDOW", self.destroy_main_window)

    def destroy_main_window(self):
        self.destroy()  # Close the application


if __name__ == "__main__":
    app = MainApplication(None)  # Pass None as the master
    app.mainloop()
