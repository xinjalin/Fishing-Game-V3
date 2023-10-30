import csv
import os
from random import randint

ASSETS_FOLDER = "assets"


class Fish:
    def __init__(self, name, keeper, fish, points_if_kept, points_if_released):
        self.name = name
        self.keeper = keeper
        self.fish = fish
        self.points_if_kept = points_if_kept
        self.points_if_released = points_if_released

    def __str__(self):
        return f"{self.name}, {self.keeper}, {self.fish}, {self.points_if_kept}, {self.points_if_released}"


def read_fish_csv(file_path=None):
    objects = []

    if file_path is None:
        file_path = os.path.join(ASSETS_FOLDER, 'fish.csv')

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for row in csv_reader:
            name, keeper, fish, points_if_kept, points_if_released = row
            obj = Fish(name, keeper, fish, points_if_kept, points_if_released)
            objects.append(obj)

    return objects


def go_fishing(fish):
    fish_names = {
        1: 'King George Whiting',
        2: 'Lost bait',
        3: 'Small Mulloway',
        4: 'Snapper',
        5: 'Large Mullet',
        6: 'Seaweed Monster (random) clump of seaweed'
    }

    dice_roll = randint(1, 6)
    fish_name = fish_names.get(dice_roll, None)

    if fish_name is not None:
        for fish_obj in fish:
            if fish_obj.name == fish_name:
                return fish_obj

    return None  # Return None if no fish is found for the random number


