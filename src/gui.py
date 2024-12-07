import tkinter as tk
from tkinter import filedialog, messagebox
from core import FileOrganizer
from duplicate_checker import DuplicateChecker
from monitor import FolderMonitor

class FileGuardianApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileGuardian")

        # Variables
        self.monitor_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()
        self.organizer = FileOrganizer()
        self.monitor = None

        # GUI Layout
        self.setup_ui()

    def setup_ui(self):
        # Folder Selection
        frame_folders = tk.Frame(self.root)
        frame_folders.pack(pady=10)
        tk.Label(frame_folders, text="Carpeta de monitoreo:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_folders, textvariable=self.monitor_folder, width=40).grid(row=0, column=1)
        tk.Button(frame_folders, text="Seleccionar", command=self.select_monitor_folder).grid(row=0, column=2)

        tk.Label(frame_folders, text="Carpeta de destino:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame_folders, textvariable=self.destination_folder, width=40).grid(row=1, column=1)
        tk.Button(frame_folders, text="Seleccionar", command=self.select_destination_folder).grid(row=1, column=2)

        # Buttons
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10)
        tk.Button(frame_buttons, text="Iniciar Monitoreo", command=self.start_monitoring).grid(row=0, column=0, padx=5)
        tk.Button(frame_buttons, text="Detener Monitoreo", command=self.stop_monitoring).grid(row=0, column=1, padx=5)
        tk.Button(frame_buttons, text="Buscar Duplicados", command=self.find_duplicates).grid(row=0, column=2, padx=5)
        tk.Button(frame_buttons, text="Organizar Carpeta", command=self.organize_folder).grid(row=0, column=3, padx=5)

    def select_monitor_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.monitor_folder.set(folder)

    def select_destination_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_folder.set(folder)

    def start_monitoring(self):
        if not self.monitor_folder.get() or not self.destination_folder.get():
            messagebox.showwarning("Error", "Selecciona carpetas de monitoreo y destino.")
            return
        if self.monitor:
            self.monitor.stop()

        self.monitor = FolderMonitor(
            source_folder=self.monitor_folder.get(),
            destination_folder=self.destination_folder.get(),
            organizer=self.organizer
        )
        self.monitor.start()
        messagebox.showinfo("Monitoreo", "Monitoreo iniciado.")

    def stop_monitoring(self):
        if self.monitor:
            self.monitor.stop()
            self.monitor = None
            messagebox.showinfo("Monitoreo", "Monitoreo detenido.")

    def find_duplicates(self):
        if not self.monitor_folder.get():
            messagebox.showwarning("Error", "Selecciona una carpeta de monitoreo.")
            return

        duplicates = DuplicateChecker.find_duplicates(self.monitor_folder.get())
        if duplicates:
            duplicates_str = "\n".join(f"{key}: {', '.join(paths)}" for key, paths in duplicates.items())
            messagebox.showinfo("Duplicados Encontrados", f"Duplicados:\n{duplicates_str}")
        else:
            messagebox.showinfo("Duplicados", "No se encontraron duplicados.")

    def organize_folder(self):
        if not self.monitor_folder.get():
            messagebox.showwarning("Error", "Selecciona una carpeta para organizar.")
            return

        self.organizer.load_rules("config/rules.json")
        results = self.organizer.organize_folder(self.monitor_folder.get())
        result_str = "\n".join(results)
        messagebox.showinfo("Organización Completa", f"Resultados:\n{result_str}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileGuardianApp(root)
    root.mainloop()
