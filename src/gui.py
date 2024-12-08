import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from core import FileOrganizer
from duplicate_checker import DuplicateChecker
from monitor import FolderMonitor
import os
import tkinter as tk
from tkinter import ttk  # Mantener ttk separado

class FileGuardianApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Guardian")
        self.root.geometry("650x400")
        
        # Establecer el icono dependiendo del sistema operativo
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
        if os.name == 'nt':  # Windows
            self.root.iconbitmap(icon_path)
        else:
            try:
                # En macOS y Linux, tkinter no soporta .ico. Usa .png o .gif
                from tkinter import PhotoImage
                icon = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'assets', 'icon.png'))
                self.root.iconphoto(False, icon)
            except Exception as e:
                print(f"Error al cargar el icono: {e}")

        # Variables
        self.monitor_folder = tb.StringVar()
        self.destination_folder = tb.StringVar()
        self.organizer = FileOrganizer()
        self.monitor = None

        # GUI Layout
        self.setup_ui()

    def setup_ui(self):
        # Crear un Frame principal con padding
        main_frame = tb.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tb.Label(main_frame, text="File Guardian", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))

        # Sección de Selección de Carpetas
        folders_frame = tb.LabelFrame(main_frame, text="Seleccionar Carpeta", padding=15)
        folders_frame.pack(fill=tk.X, pady=10)

        # Carpeta de Monitoreo
        self.create_folder_selection(folders_frame, "", self.monitor_folder, 0)

        # Carpeta de Destino
        # self.create_folder_selection(folders_frame, "Carpeta de Destino:", self.destination_folder, 1)

        # Sección de Botones
        buttons_frame = tb.Frame(main_frame)
        buttons_frame.pack(pady=20)

        # Botones con estilo y iconos
        btn_style = {"bootstyle": "primary-outline", "padding": (10, 5)}
        # tb.Button(buttons_frame, text="Iniciar Monitoreo", command=self.start_monitoring, **btn_style).grid(row=0, column=0, padx=5, pady=5)
        # tb.Button(buttons_frame, text="Detener Monitoreo", command=self.stop_monitoring, **btn_style).grid(row=0, column=1, padx=5, pady=5)
        tb.Button(buttons_frame, text="Buscar Duplicados", command=self.find_duplicates, **btn_style).grid(row=0, column=2, padx=5, pady=5)
        tb.Button(buttons_frame, text="Organizar Carpeta", command=self.organize_folder, **btn_style).grid(row=0, column=3, padx=5, pady=5)

        # Área de Estado
        self.status_var = tb.StringVar(value="Listo")
        status_bar = tb.Label(main_frame, textvariable=self.status_var, bootstyle="info", anchor="w")
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def create_folder_selection(self, parent, label_text, variable, row):
        tb.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=5)
        entry = tb.Entry(parent, textvariable=variable, width=50)
        entry.grid(row=row, column=1, padx=10, pady=5)
        tb.Button(parent, text="Seleccionar", command=lambda: self.select_folder(variable)).grid(row=row, column=2, padx=5, pady=5)

    def select_folder(self, variable):
        folder = filedialog.askdirectory()
        if folder:
            variable.set(folder)
            self.update_status(f"Seleccionada carpeta: {folder}")

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
        self.update_status("Monitoreo iniciado.")
        messagebox.showinfo("Monitoreo", "Monitoreo iniciado.")

    def stop_monitoring(self):
        if self.monitor:
            self.monitor.stop()
            self.monitor = None
            self.update_status("Monitoreo detenido.")
            messagebox.showinfo("Monitoreo", "Monitoreo detenido.")
        else:
            messagebox.showinfo("Monitoreo", "No hay monitoreo activo.")

    def find_duplicates(self):
        if not self.monitor_folder.get():
            messagebox.showwarning("Error", "Selecciona una carpeta de monitoreo.")
            return

        duplicates = DuplicateChecker.find_duplicates(self.monitor_folder.get())
        if duplicates:
            duplicates_str = "\n".join(f"{key}: {', '.join(paths)}" for key, paths in duplicates.items())
            self.show_scrollable_message("Duplicados Encontrados", f"Duplicados:\n{duplicates_str}")
            self.update_status("Duplicados encontrados.")
        else:
            messagebox.showinfo("Duplicados", "No se encontraron duplicados.")
            self.update_status("No se encontraron duplicados.")

    def organize_folder(self):
        if not self.monitor_folder.get():
            messagebox.showwarning("Error", "Selecciona una carpeta para organizar.")
            return

        try:
            self.organizer.load_rules("config/rules.json")
            results = self.organizer.organize_folder(self.monitor_folder.get())
            result_str = "\n".join(results)
            self.show_scrollable_message("Organización Completa", f"Resultados:\n{result_str}")
            self.update_status("Organización completada.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al organizar la carpeta: {e}")
            self.update_status("Error en la organización.")

    def show_scrollable_message(self, title, message):
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("500x400")
        top.grab_set()

        text_area = tk.Text(top, wrap='word')
        text_area.insert('1.0', message)
        text_area.config(state='disabled')
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tb.Scrollbar(top, command=text_area.yview)
        text_area['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side='right', fill='y')

    def update_status(self, message):
        self.status_var.set(message)

if __name__ == "__main__":
    # Crear la ventana principal con ttkbootstrap
    root = tb.Window(themename="flatly")  # Usa tb.Window en lugar de ttk.Window
    app = FileGuardianApp(root)
    root.mainloop()
