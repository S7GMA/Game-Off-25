import os

# Define folder structure
folders = [
    "assets/sounds",
    "assets/images",
    "assets/fonts",
    "levels"
]

# Base files to help organize the project
base_files = [
    "main.py",
    "settings.py",
    "player.py",
    "enemy.py",
    "level.py",
    "sound.py"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✅ Created folder: {folder}")

# Create empty base files if they don't exist
for file in base_files:
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("# " + file + " - placeholder\n")
        print(f"📝 Created file: {file}")

print("\n🎮 Project structure ready! Drop your assets and code in.")
