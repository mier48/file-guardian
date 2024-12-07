from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderMonitor:
    def __init__(self, source_folder, destination_folder, organizer):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.organizer = organizer
        self.observer = Observer()

    def start(self):
        event_handler = self.FileHandler(self.organizer, self.destination_folder)
        self.observer.schedule(event_handler, path=self.source_folder, recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    class FileHandler(FileSystemEventHandler):
        def __init__(self, organizer, destination_folder):
            self.organizer = organizer
            self.destination_folder = destination_folder

        def on_created(self, event):
            if not event.is_directory:
                result = self.organizer.organize_file(event.src_path, self.destination_folder)
                print(f"Archivo organizado: {result}")
