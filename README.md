# Pokémon Storage System with PyQt and PokéAPI Integration

A simple, fun desktop application built using PyQt that allows users to store Pokémon details, fetch and display their sprites from the PokéAPI, and save/load Pokémon data to/from a file. The app provides a graphical user interface (GUI) to interact with Pokémon data.

## Features

- **Add Pokémon**: Users can add Pokémon by entering their name, primary type, secondary type, and level.
- **List Pokémon**: The app lists all the Pokémon that the user has added.
- **Display Sprites**: When a Pokémon is selected from the list, its sprite is fetched from the PokéAPI and displayed in the GUI.
- **Save/Load Pokémon Data**: Pokémon data can be saved to and loaded from a text file for persistent storage.

## Screenshots

> Add screenshots of your application here (use `![Screenshot description](image_path)`).

## Technologies Used

- **PyQt5**: Used for the graphical user interface.
- **Requests**: Used to fetch Pokémon sprites from the [PokéAPI](https://pokeapi.co/).
- **PokéAPI**: Public API for retrieving Pokémon data.

## Requirements

To run this application, you need to install the following dependencies:

1. **Python 3.x**: Ensure that you have Python 3.x installed on your machine.
2. **PyQt5**: Install PyQt5 for the graphical interface.
3. **Requests**: Install the requests module to fetch data from the PokéAPI.

You can install the required dependencies by running:

```bash
pip install PyQt5 requests
