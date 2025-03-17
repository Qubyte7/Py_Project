import os
import ctypes
import winreg
import sys
import subprocess

# Configuration (must match your original app's settings)
STARTUP_NAME = "ncat.exe"
NMAP_PATH_ENTRY = r'C:\Program Files (x86)\Nmap'


def check_admin():
    """Check if running as administrator"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def remove_startup_entry():
    """Remove executable from startup folder"""
    try:
        startup_path = os.path.join(
            os.getenv('APPDATA'),
            'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup',
            STARTUP_NAME
        )

        if os.path.exists(startup_path):
            os.remove(startup_path)
            print(f"Removed startup entry: {startup_path}")
        else:
            print("No startup entry found")
    except Exception as e:
        print(f"Error removing startup entry: {str(e)}")


def remove_nmap_from_path():
    """Remove Nmap from system PATH"""
    try:
        key_path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            path_value = winreg.QueryValueEx(key, 'Path')[0]

            if NMAP_PATH_ENTRY in path_value:
                new_path = path_value.replace(NMAP_PATH_ENTRY + ';', '')
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
                print("Removed Nmap from system PATH")

                # Refresh environment variables
                ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x02, 5000, None)
            else:
                print("Nmap not found in PATH")
    except Exception as e:
        print(f"Error modifying PATH: {str(e)}")


def main():
    if not check_admin():
        # Re-run with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("=== Cleaning Persistence Mechanisms ===")

    # 1. Remove startup entry
    remove_startup_entry()

    # 2. Clean PATH environment variable
    remove_nmap_from_path()

    # 3. Additional cleanup tasks could be added here
    print("\nCleanup complete. Recommended actions:")
    print("- Reboot your computer")
    print("- Manually uninstall Nmap if needed")


if __name__ == "__main__":
    main()