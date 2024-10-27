# CHESS_PYGAME.PY

# STEP BY STEP

1. Install Dependencies
Open a terminal and install the required libraries by running:

pip install python-chess pygame

2. Download Stockfish
Go to Stockfish’s official website to download the latest version of Stockfish.
After downloading, extract the ZIP file.

3. Set Up Stockfish Path in Your Code
Locate stockfish.exe in the extracted folder.
Open chess_bot.py, and set the path to stockfish.exe in line 77.

Example: If stockfish.exe is in C:/Users/Agent Ezra/OneDrive/Pict/Docs/Ezra Chess/stockfish-windows-x86-64-avx2/stockfish/, set the path as follows:

Chess_Bot.py Line 77
engine_path = "C:/Users/Agent Ezra/OneDrive/Pict/Docs/Ezra Chess/stockfish-windows-x86-64-avx2/stockfish/stockfish.exe"


# REMINDERS

* Python Installation
Ensure Python is installed on your PC/Laptop. If not, download and install it from python.org.

* Path Formatting
When copying the path to stockfish.exe, change any \ to / in the path to avoid errors. For example:

C:\path\to\stockfish.exe    -->    C:/path/to/stockfish.exe

* Picking Color at Start
When running the program, it prompts you to choose a color (w for white, b for black). If you see only a black screen, ensure you select a color in the terminal before continuing.

