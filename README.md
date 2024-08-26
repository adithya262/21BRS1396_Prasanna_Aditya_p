Turn-Based Game

This is a simple turn-based game where two players take turns moving characters on a 5x5 board. The game is played over a WebSocket connection, with a Python server handling the game logic and a web-based client providing the user interface.

Features

Two-player turn-based game.
Different characters with unique movement patterns.
Displays a guide for character movements at the start of the game.
Announces the winner with a stylish animation when a player wins.
Displays a message when a character kills an enemy character.
Setup Instructions

Prerequisites
Python 3.x
Node.js (optional, for managing frontend dependencies)
A modern web browser

Server Setup:
Clone the Repository:
bash:
git clone https://github.com/adithya262/WebSocket-Turn-Based-Game.git
cd turn-based-game
Create a Virtual Environment (optional but recommended):

bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install Required Python Packages:
bash:
pip install websockets

Run the Server:
bash:
python server.py
The server will start and listen on ws://localhost:12345.

Client Setup:
Navigate to the client Directory:
bash
cd client
Install Dependencies:
If you have Node.js installed, you can install the dependencies using npm. This step is optional if you're not managing frontend dependencies with npm.

bash:
npm install
Run the Client:
Open index.html in a web browser. You can do this directly by double-clicking the file or by serving it through a simple HTTP server.

If you have Python installed, you can serve the file using Python's built-in HTTP server:

bash:
python -m http.server
Then, navigate to http://localhost:8000 in your web browser.

How to Play:
The game starts with a guide showing how each character moves. The guide will fade away after 5 seconds.
Players take turns moving their characters. To move a character:
Click on your character to select it.
Choose a direction from the movement options displayed.
If a character kills an enemy, the game will display a message indicating which character was killed.
The game ends when all characters of one player are killed, and the winner is announced with a stylish animation.
Game Logic:
Heroes have special movement rules:
Hero1 moves in straight lines.
Hero2 moves diagonally.
Pawns move one step in any direction.
The game checks for a winner after each move. If a player has no remaining characters, the opponent wins.

Author:
Prasanna Aditya P
github.com/adithya262

Disclaimer: If the game board does not show or appear when you open the "index.html" check whether the "server.py" is running the background.
If the above code does not run on command prompt or terminal run the "server.py" and "index.html" in VS code along with "Live Server 5.7.2V" extension