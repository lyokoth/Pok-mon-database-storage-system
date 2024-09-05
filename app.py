import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QListWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap

class Pokemon:
    def __init__(self, name, p_type1, p_type2, level):
        self.name = name
        self.p_type1 = p_type1
        self.p_type2 = p_type2
        self.level = level 

    def __repr__(self):
        return f"{self.name} (Type: {self.p_type1}, {self.p_type2}, Level: {self.level})"

class PokemonStorage:
    def __init__(self):
        self.storage = []

    def add_pokemon(self, pokemon):
        self.storage.append(pokemon)

    def list_pokemon(self):
        return [f"{pokemon.name} - Level: {pokemon.level}" for pokemon in self.storage]

    def get_pokemon_by_name(self, name):
        for pokemon in self.storage:
            if pokemon.name.lower() == name.lower():
                return pokemon
        return None

    def save_to_file(self, filename="pokemon_storage.txt"):
        with open(filename, "w") as file:
            for pokemon in self.storage:
                file.write(f"{pokemon.name}, {pokemon.p_type1}, {pokemon.p_type2}, {pokemon.level}\n")

    def load_file(self, filename="pokemon_storage.txt"):
        try:
            with open(filename, "r") as file:
                for line in file:
                    name, p_type1, p_type2, level = line.strip().split(", ")
                    self.add_pokemon(Pokemon(name, p_type1, p_type2, int(level)))
        except FileNotFoundError:
            return "File not found, starting with an empty storage."


# Function to get Pokémon sprite from PokéAPI
def get_pokemon_sprite(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        sprite_url = data['sprites']['front_default']
        return sprite_url
    else:
        return None


class PokemonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.storage = PokemonStorage()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Image display
        self.sprite_label = QLabel(self)
        self.sprite_label.setPixmap(QPixmap("default_pokemon.png"))

        # Pokémon input fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Pokémon Name")
        self.type1_input = QLineEdit(self)
        self.type1_input.setPlaceholderText("Enter Primary Type")
        self.type2_input = QLineEdit(self)
        self.type2_input.setPlaceholderText("Enter Secondary Type (optional)")
        self.level_input = QLineEdit(self)
        self.level_input.setPlaceholderText("Enter Pokémon Level")

        # Add Pokémon button
        self.add_button = QPushButton("Add Pokémon", self)
        self.add_button.clicked.connect(self.add_pokemon)

        # List of Pokémon
        self.pokemon_list = QListWidget(self)
        self.pokemon_list.clicked.connect(self.display_pokemon_sprite)

        # Save/Load buttons
        self.save_button = QPushButton("Save to File", self)
        self.save_button.clicked.connect(self.save_storage)
        self.load_button = QPushButton("Load from File", self)
        self.load_button.clicked.connect(self.load_storage)

        # Layout arrangement
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.type1_input)
        input_layout.addWidget(self.type2_input)
        input_layout.addWidget(self.level_input)
        input_layout.addWidget(self.add_button)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.load_button)

        layout.addLayout(input_layout)
        layout.addWidget(self.sprite_label)
        layout.addWidget(self.pokemon_list)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.setWindowTitle("Pokémon Storage System")

    def add_pokemon(self):
        name = self.name_input.text()
        p_type1 = self.type1_input.text()
        p_type2 = self.type2_input.text() if self.type2_input.text() else "N/A"
        level = self.level_input.text()

        if not name or not p_type1 or not level.isdigit():
            QMessageBox.warning(self, "Input Error", "Please enter valid details!")
            return

        # Add Pokémon to storage
        new_pokemon = Pokemon(name, p_type1, p_type2, int(level))
        self.storage.add_pokemon(new_pokemon)

        # Clear input fields and update list
        self.name_input.clear()
        self.type1_input.clear()
        self.type2_input.clear()
        self.level_input.clear()

        self.update_pokemon_list()

    def update_pokemon_list(self):
        self.pokemon_list.clear()
        for pokemon in self.storage.list_pokemon():
            self.pokemon_list.addItem(pokemon)

    def display_pokemon_sprite(self):
        selected_item = self.pokemon_list.currentItem()
        if selected_item:
            pokemon_name = selected_item.text().split(" - ")[0]
            sprite_url = get_pokemon_sprite(pokemon_name)

            if sprite_url:
                image = QPixmap()
                image.loadFromData(requests.get(sprite_url).content)
                self.sprite_label.setPixmap(image)
            else:
                QMessageBox.warning(self, "Sprite Error", f"Could not retrieve sprite for {pokemon_name}")

    def save_storage(self):
        self.storage.save_to_file()
        QMessageBox.information(self, "Success", "Pokémon storage saved successfully!")

    def load_storage(self):
        self.storage.load_file()
        self.update_pokemon_list()
        QMessageBox.information(self, "Success", "Pokémon storage loaded successfully!")


# Running the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PokemonApp()
    window.show()
    sys.exit(app.exec_())
