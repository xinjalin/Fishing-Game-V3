import csv
import os
import bcrypt

ASSETS_FOLDER = "assets"


def create_csv():
    fieldnames = ['username', 'password_hash']
    try:
        # Create the "assets" folder if it doesn't exist
        os.makedirs(ASSETS_FOLDER, exist_ok=True)

        # Define the file path within the "assets" folder
        file_path = os.path.join(ASSETS_FOLDER, 'user_data.csv')

        # Create the CSV file
        with open(file_path, 'x', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass


def save_to_csv(user_data):
    fieldnames = ['username', 'password_hash']
    try:
        file_path = os.path.join(ASSETS_FOLDER, 'user_data.csv')

        with open(file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(user_data)
    except FileNotFoundError:
        pass


def is_present_in_csv(username):
    try:
        file_path = os.path.join(ASSETS_FOLDER, 'user_data.csv')

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    return True
    except FileNotFoundError:
        pass


def get_password(username):
    try:
        file_path = os.path.join(ASSETS_FOLDER, 'user_data.csv')

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    stored_hash = row['password_hash']
                    return stored_hash
    except FileNotFoundError:
        pass


def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_text_password.encode(), salt).decode()


def check_password(plain_text_password, password_hash):
    return bcrypt.checkpw(plain_text_password.encode(), password_hash.encode())
