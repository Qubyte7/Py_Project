import tkinter as tk
from tkinter import messagebox
import os


def remove_startup_entry():
    """Remove 'WindowsGameHost.exe' from the Startup folder."""
    # Construct the path to the Startup folder
    startup_path = os.path.join(
        os.getenv('APPDATA'),
        'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
    )
    target_file = os.path.join(startup_path, 'WindowsGameHost.exe')

    # Check if the file exists
    if not os.path.exists(target_file):
        messagebox.showinfo("Info", "The startup entry was not found.")
        return

    # Attempt to delete the file
    try:
        os.remove(target_file)
        messagebox.showinfo("Success", "Successfully removed 'WindowsGameHost.exe' from startup.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove startup entry: {str(e)}")


def main():
    """Create and run the GUI for the removal app."""
    root = tk.Tk()
    root.title("Remove Startup Entry")

    # Display a message explaining the action
    label = tk.Label(root, text="This will remove 'WindowsGameHost.exe' from your startup programs.")
    label.pack(pady=10)

    # Add a Remove button
    remove_button = tk.Button(root, text="Remove", command=remove_startup_entry)
    remove_button.pack(side=tk.LEFT, padx=20)

    # Add a Cancel button
    cancel_button = tk.Button(root, text="Cancel", command=root.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=20)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()