# gym-dash
Gym Progress Tracker
====================================================
  GYM DASH — Personal Progress Tracker
====================================================

QUICK START
-----------
1. Install Python 3  (only needed once)
   -> https://www.python.org/downloads/
   -> During install, CHECK "Add Python to PATH"

2. Double-click  start.bat

3. Your browser opens to  http://localhost:8181

That's it. The app runs entirely on your computer —
no internet required after setup.


STOPPING THE SERVER
-------------------
Click the server window and press  Ctrl + C, then Y.


YOUR DATA
---------
All logs are saved as plain JSON files inside the
  data\  folder, one file per day:

  data\2026-06-11.json
  data\2026-06-10.json
  ...

You can open these in any text editor (Notepad, VS Code).

config.json  holds your personal settings, habits,
goals, split exercises, and meal plans.


MOVING TO A NEW LAPTOP
-----------------------
Copy this entire folder to the new machine, install
Python 3, and double-click start.bat. All your history
moves with you.


TROUBLESHOOTING
---------------
"Python not found"   -> Re-install Python and check
                        "Add Python to PATH"

"Address already in use" -> Another copy is already
                        running. Close that window first,
                        or restart your computer.

"Server unavailable" in the app -> Make sure start.bat
                        is running (server window open).


PORT
----
Default: 8181
To change, open server.py and edit the PORT = 8181 line.
====================================================
