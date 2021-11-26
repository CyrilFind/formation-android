import os
import glob

for filename in glob.glob("tp/TP*.md"):
    with open(filename, 'r+') as file:
        content = file.read()
        file.seek(0)
        basename = os.path.basename(filename)
        name = os.path.splitext(basename)[0]
        file.write(f"id: {name}\n" + content)