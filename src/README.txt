(a) Program summary
Program Description
This project is a Python-based Roulette game with a Power Round twist. The game simulates a simplified roulette experience where players place bets, spin the wheel, and win or lose chips based on standard roulette rules. Periodically, a Power Round activates, modifying payouts through special effects such as multipliers, bonus spins, or streak-based bonuses.
The goal of the project is not only to create an interactive game, but also to demonstrate modular programming, object-oriented design, data tracking, and game balancing through analytics and simulation.

Main Features
Standard roulette wheel with number and color outcomes
Multiple bet types (color, number, etc.)
Power Round system using a strategy pattern
Fairness caps to prevent extreme payouts
Persistent logging of every round (JSON + CSV)
Analytics system to evaluate expected value (EV) and balance

Visual & Interactive Components
Pygame window with:
Roulette wheel placeholder
“Spin” button
Betting area
Status text for win/loss and Power Round activation
Visual indicator when Power Round triggers (text or border flash)
End-of-session statistics displayed or saved as plots

(b) Setup & Run Instructions
Required Libraries
Make sure Python 3.9+ is installed.
Install required packages using pip:
pip install pygame matplotlib
(Standard Python libraries such as random, csv, json, and statistics are included by default.)

Project File Structure
project/
analytics.py
display.py
game.py
main.py
power.py
settings.py
state.py
storage.py

How to Run the Program
Option 1 — Run the Game
python main.py
Opens the Pygame window
Allows the user to place bets and spin the wheel
Power Rounds activate automatically during gameplay
Option 2 — Run Analytics Simulation
python main.py --simulate 10000
Runs 10,000 automated rounds
Saves results to CSV and JSON files
Generates graphs for bankroll and outcome distribution
Generated files will appear in the project folder.

(c) Team Member Contributions
Member 1 — Game Engine & Roulette Logic
Implemented the roulette wheel and spin mechanics
Built bet evaluation and base payout calculations
Provided core game logic used by other modules

Member 2 — User Interface & Game Loop
Designed the Pygame interface
Implemented buttons, betting inputs, and status text
Integrated game loop with logic and power systems
Displayed Power Round effects visually

Member 3 — Power System, Logging & Analytics
Designed and implemented the Power Round system using a strategy pattern
Built the PowerManager with trigger logic and fairness caps
Created the HistoryLog to store round-by-round data
Developed the analytics and simulation tools to test balance and expected value
Integrated backend systems with the main game loop
