Asteroids — Python + Pygame
A modern, smooth, and fully playable remake of the classic Asteroids arcade game.
Built with Python and Pygame, this project features responsive controls, wave‑based difficulty, explosions, scoring, and a packaged Windows executable.

🚀 Gameplay Overview
Pilot your ship through an asteroid field, destroy incoming rocks, and survive as long as possible.
Each wave increases difficulty by spawning more asteroids.
Controls
|  |  | 
|  |  | 
|  |  | 
|  |  | 
|  |  | 
|  |  | 



🛠️ Running From Source
Requirements
- Python 3.10–3.12
- Pygame 2.6+
Install dependencies
pip install pygame


Run the game
python main.py



🪟 Windows Executable
A pre‑built Windows .exe is available in the dist/ folder.
No Python installation required — just run:
dist/main.exe



📁 Project Structure
asteroids/
│
├── main.py
├── player.py
├── asteroid.py
├── shot.py
├── explosion.py
├── utils.py
│
├── assets/
│   ├── ship.png
│   ├── explosion.png
│   └── ...
│
├── highscores.json
├── README.md
└── .gitignore



🧱 Building the EXE (Developer Notes)
This project is developed inside WSL, but compiled using Windows Python 3.12.
Build command
"/mnt/c/Users/peck_/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0/LocalCache/local-packages/Python312/Scripts/pyinstaller.exe" \
    --onefile --windowed --collect-all pygame main.py


The executable will appear in:
dist/main.exe


Copy EXE to Windows
cp dist/main.exe /mnt/c/Users/peck_/Desktop/



🏆 Features
- Smooth ship movement with rotation + thrust
- Screen wrapping
- Bullet shooting
- Asteroid splitting logic
- Explosion animations
- Wave‑based difficulty scaling
- Score + high‑score saving
- Packaged Windows executable

📜 License
This project is released for educational and personal use.
Feel free to fork, modify, and experiment.

👤 Author
Picotazo AKA: Peck
Python developer, game tinkerer, and arcade enthusiast.


