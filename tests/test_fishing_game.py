from src.fishing_game import *

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TEST_ASSETS_FOLDER = "test_assets"
FISH_CSV = "fish.csv"


def test_fish_str_representation():
    fish = Fish('Test Fish', 'Yes', 'Fish', 5, 10)

    assert str(fish) == "Test Fish, Yes, Fish, 5, 10"


def test_read_fish_csv():
    file_path = os.path.join(CURRENT_DIRECTORY, TEST_ASSETS_FOLDER, FISH_CSV)
    fish_list = read_fish_csv(file_path)

    assert len(fish_list) > 0
    assert len(fish_list) == 6


def test_go_fishing():
    file_path = os.path.join(CURRENT_DIRECTORY, TEST_ASSETS_FOLDER, FISH_CSV)
    fish_list = read_fish_csv(file_path)
    caught_fish = go_fishing(fish_list)

    assert isinstance(caught_fish, Fish) or caught_fish is None
