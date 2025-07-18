
import os
import shutil
import time
from watchdog.observers import Observer  # type: ignore
from watchdog.events import FileSystemEventHandler  # type: ignore

source_dir = r"C:\Users\Administrator\Downloads"
dest_dir_docs = r"C:\Users\Administrator\OneDrive\Documents\Important Documents"
dest_dir_pdf = r"C:\Users\Administrator\OneDrive\Documents\Important PDF Files"
dest_dir_music = r"C:\Users\Administrator\Music\Bops"
dest_dir_images = r"C:\Users\Administrator\OneDrive\Pictures\Meme Folder"
dest_dir_videos = r"C:\Users\Administrator\Videos\Video Vault"

for folder in [dest_dir_docs, dest_dir_pdf, dest_dir_music, dest_dir_images, dest_dir_videos]:
    os.makedirs(folder, exist_ok=True)

def make_unique(destination, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(destination, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1
    return new_filename

def move_file(filepath, filename):
    if filename.endswith('.docx') or filename.endswith('.txt'):
        dest = dest_dir_docs
    elif filename.endswith('.pdf'):
        dest = dest_dir_pdf
    elif filename.endswith('.mp3') or filename.endswith('.wav'):
        dest = dest_dir_music
    elif filename.endswith('.jpg') or filename.endswith('.png'):
        dest = dest_dir_images
    elif filename.endswith('.mp4') or filename.endswith('.mov'):
        dest = dest_dir_videos 
    else:
        return
    
    if not os.path.exists(dest):
        print(f"Destination folder does not exist: {dest}")
        return
    new_filename = make_unique(dest, filename)
    destination_path = os.path.join(dest, new_filename)

    try:
        time.sleep(2)
        if os.path.exists(filepath):
            shutil.move(filepath, destination_path)
            print(f"Moved {filename} to {dest}")
        else:
            print(f"File {filename} does not exist at {filepath} when attempting to move.")
    except Exception as e:
        print(f"Error moving {filename}: {e}")

class MyHandler(FileSystemEventHandler): 
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    move_file(entry.path, entry.name)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    observer.start()
    print("Monitoring started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()