import tkinter as tk
from src.utility import *
from src.fishing_game import *


class LoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Login")
        self.resizable(False, False)

        # GUI components for Login Window
        self.username_label = tk.Label(self, text="Username")
        self.password_label = tk.Label(self, text="Password")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")  # Show asterisks for password input
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.home_button = tk.Button(self, text="Home", command=self.home)
        self.infoLabel = tk.Label(self, text="")

        # Position GUI components on the Login Window
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.login_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="w")
        self.home_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="e")
        self.infoLabel.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="n")

    def login(self):
        # login logic here
        username = self.entry_username.get()
        password = self.entry_password.get()

        if is_present_in_csv(username):
            csv_user_data = get_password(username)
            is_match = check_password(password, csv_user_data)
            if is_match:
                self.withdraw()
                game_window = GameWindow(self, username)
                game_window.protocol("WM_DELETE_WINDOW", self.destroy_window)
            else:
                # not is_match
                self.infoLabel.config(text="Invalid Password")
        else:
            # not present in csv
            self.infoLabel.config(text=f"username: {username} dose not exist.")

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
        self.resizable(False, False)

        # GUI components for Login Window
        self.username_label = tk.Label(self, text="Username")
        self.password_label = tk.Label(self, text="Password")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self)
        self.login_button = tk.Button(self, text="Register", command=self.register)
        self.home_button = tk.Button(self, text="Home", command=self.home)
        self.infoLabel = tk.Label(self, text="")

        # Position GUI components on the Login Window
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_username.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.login_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="w")
        self.home_button.grid(row=2, column=1, columnspan=1, pady=10, padx=10, sticky="e")
        self.infoLabel.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="n")

    def register(self):
        # register logic here
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "" or password == "":
            self.infoLabel.config(text="username or password not supplied")
        else:
            if is_present_in_csv(username):  # user already exists
                self.infoLabel.config(text=f"username: {username} all ready exists")
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
    def __init__(self, master, username):
        super().__init__(master)
        self.title("Fishing Game")
        self.geometry("585x175")
        self.resizable(False, False)

        self.username_ref = username
        self.fish = read_fish_csv()
        self.captured_fish = []
        self.result_of_fishing = None
        self.player_score = tk.IntVar(value=0)  # using IntVar so I can use get and set methods

        self.infoLabel = tk.Label(self, text="", width=80, relief="ridge")
        self.player_score_Label = tk.Label(self, text=self.player_score.get())
        self.user_info_Label = tk.Label(self, text=f"Player: {self.username_ref}")
        self.user_info_score_Label = tk.Label(self, text=f"Score:")
        self.go_fishing_btn = tk.Button(self, text="Cast Rod", command=self.cast_rod, width=10)
        self.keep_fish_btn = tk.Button(self, text="Keep Fish", command=self.keep_fish, width=10)
        self.release_fish_btn = tk.Button(self, text="Release Fish", command=self.release_fish, width=10)
        self.see_fish_btn = tk.Button(self, text="See Kept Fish", command=self.see_fish, width=10)

        self.infoLabel.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="n")
        self.user_info_score_Label.grid(row=0, column=1, pady=10, sticky="e")
        self.player_score_Label.grid(row=0, column=2, pady=10, sticky="w")
        self.user_info_Label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")
        self.go_fishing_btn.grid(row=2, column=0, padx=10, pady=5, sticky="n")
        self.keep_fish_btn.grid(row=2, column=1, padx=10, pady=5, sticky="n")
        self.release_fish_btn.grid(row=2, column=2, padx=10, pady=5, sticky="n")
        self.see_fish_btn.grid(row=4, column=1, padx=10, pady=5, sticky="n")

    def cast_rod(self):
        self.result_of_fishing = go_fishing(self.fish)
        self.infoLabel.config(text=self.result_of_fishing.name)
        if self.result_of_fishing.name == "Lost bait":
            self.update_player_score("keep")
            self.result_of_fishing = None
            self.keep_fish_btn.config(state="disabled")
            self.release_fish_btn.config(state="disabled")
        else:
            self.keep_fish_btn.config(state="normal")
            self.release_fish_btn.config(state="normal")

    def keep_fish(self):
        if self.result_of_fishing is None:
            pass
        else:
            self.infoLabel.config(text=f"You Kept the ({self.result_of_fishing.name})")
            self.update_player_score("keep")
            self.captured_fish.append(self.result_of_fishing)
            self.result_of_fishing = None  # resets result_of_fishing variable after appending to the list

    def release_fish(self):
        if self.result_of_fishing is None:
            pass
        else:
            self.infoLabel.config(text=f"You Released the ({self.result_of_fishing.name})")
            self.update_player_score("release")
            self.result_of_fishing = None

    def see_fish(self):
        fish_list_window = FishListWindow(self, self.captured_fish, self.player_score)
        fish_list_window.grab_set()

    def update_player_score(self, flag):
        current_score = self.player_score.get()
        if flag == "keep":
            new_score = current_score + int(self.result_of_fishing.points_if_kept)
            self.player_score.set(new_score)
        elif flag == "release":
            new_score = current_score + int(self.result_of_fishing.points_if_released)
            self.player_score.set(new_score)

        self.player_score_Label.config(text=self.player_score.get())


class FishListWindow(tk.Toplevel):
    def __init__(self, master, captured_fish, player_score_ref):
        super().__init__(master)
        self.title("List of Captured Fish")
        self.geometry("300x250")
        self.resizable(False, False)

        self.captured_fish = captured_fish
        self.player_score_ref = player_score_ref

        self.listbox = tk.Listbox(self, width=45)
        self.remove_button = tk.Button(self, text="Remove Fish", command=self.remove_fish, width=10)
        self.close_button = tk.Button(self, text="Close", command=self.destroy, width=10)

        for fish in self.captured_fish:
            self.listbox.insert(tk.END, fish.name)

        self.listbox.pack(padx=10, pady=10)
        self.remove_button.pack(padx=10, pady=5)
        self.close_button.pack(padx=10, pady=5)

    def remove_fish(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            removed_fish = self.captured_fish.pop(index)
            self.listbox.delete(index)
            # remove player initial score for keeping the fish then give the score for releasing the fish
            self.player_score_ref.set(self.player_score_ref.get() - int(removed_fish.points_if_kept))
            self.player_score_ref.set(self.player_score_ref.get() + int(removed_fish.points_if_released))
            self.master.player_score_Label.config(text=self.player_score_ref.get())
            self.master.infoLabel.config(text=f"You changed your mind and released ({removed_fish.name})")


class MainApplication(tk.Tk):
    def __init__(self, master):
        super().__init__(master)
        self.title("Fishing Game")
        self.geometry("300x100")
        self.resizable(False, False)

        self.photo = tk.PhotoImage(file="assets/fish-304097_640.gif")

        # Restrict the size of the image
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
