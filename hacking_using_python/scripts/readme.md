# Snake Game with Reverse Shell

This project combines a classic Snake game implemented using Python's Turtle graphics with a reverse shell feature for educational purposes. The reverse shell establishes a connection to a specified IP and port, potentially allowing remote command execution on the host machine. **This is intended for learning purposes only and should only be used in controlled environments with explicit consent.**

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Setup](#setup)
5. [How It Works](#how-it-works)
6. [Usage](#usage)
7. [Configuration](#configuration)
8. [Removal Tool](#removal-tool)
9. [Disclaimer](#disclaimer)

---

## Project Overview
The project integrates two primary components:
- **Snake Game**: A traditional Snake game where the player navigates a snake to eat food, increasing its length and score, until it collides with the wall or itself.
- **Reverse Shell**: A background process that connects to a remote IP and port, enabling command execution via `ncat` (from Nmap).

Additional functionalities include:
- Silent installation of Nmap (for `ncat`) if not already present.
- Persistence by copying the script to the Windows Startup folder.
- A user notification dialog to inform and gain consent before executing potentially intrusive actions.

---

## Features
- **Snake Game**:
  - Built with Python’s Turtle graphics.
  - Score tracking and game-over detection.
  - Restart option after game over.
- **Reverse Shell**:
  - Connects to a configurable IP and port using `ncat`.
  - Runs in a separate thread to avoid disrupting the game.
- **System Modifications**:
  - Automatically installs Nmap silently if `ncat` is missing.
  - Adds the script to the Windows Startup folder for persistence.
- **User Notification**:
  - Displays a dialog explaining the script’s actions (Nmap installation, persistence, reverse shell) and requires user consent.

---

## Requirements
- **Python 3.x**
- **Python Libraries**:
  - `turtle` (included in Python standard library)
  - `random` (included in Python standard library)
  - `freegames` (install via `pip install freegames`)
  - `python-dotenv` (install via `pip install python-dotenv`)
  - `tkinter` (included in Python standard library for dialogs)
- **Nmap**: Required for `ncat`; installed automatically if not found.
- **Operating System**: Windows (due to Startup folder and registry modifications).

---

## some commands involved 
### <ins>description</ins>
For a better reverse shell persistence you must detach it from the command line 
bellow are the commands you can use to check and terminate the ncat connection it you want

***check ncat connection*** :   <sup>tasklist | findstr "ncat" </sup> *(windows)*
                                <sup>tasklist | grep "ncat" </sup> *(linux)*

***terminate ncat connection*** :   <sup>taskkill /IM ncat.exe /F </sup> *(windows)*
                                    <sup>pkill firefox </sup> *(linux)* 


## For disguissing our *executable_file* we use **pyinstaller** 
### covering our *executable_file* icon image
***command*** : **<sub>pyinstaller --onefile --noconsole --icon= < Your_Image_icon.ico >  --distpath < path to the storage > < your_script.py > </sub>**

**flag explanation** : 
🔹 --distpath → Final .exe location.
🔹 --workpath → Temporary PyInstaller files.

<ins> example of command </ins>

pyinstaller --onefile --noconsole --icon=./images/cover.ico --distpath "C:\Users\user\Downloads\cybersec\Py_Project\hacking_using_python\final_output" --workpath "C:\Users\user\Downloads\cybersec\Py_Project\hacking_using_python\final_output" reverse_shell.py
