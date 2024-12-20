import json
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from save import RobotPosition, CameraSettings, save_to_json, load_from_json, delete_object_from_json
from dobot import DobotController
from camTk import CameraProcessor
import threading
from robotControl import init_robot_ui



class RobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Position & Camera Settings Manager")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        self.robot_frame = tk.Frame(self.notebook)
        self.camera_frame = tk.Frame(self.notebook)

        self.notebook.add(self.robot_frame, text="Robot Control")
        self.notebook.add(self.camera_frame, text="Camera Settings")

        init_robot_ui(self.robot_frame)
        self.camera_processor = CameraProcessor(self.camera_frame)

        self.continue_flag = [True]  # Ініціалізація атрибута continue_flag
        self.camera_thread = None

        """Ініціалізація підключення до Dobot."""
        try:
            self.dobot_controller = DobotController()
            messagebox.showinfo("Dobot Connected", "Dobot successfully connected.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect Dobot: {e}")


    def open_cam_view(self):
        self.continue_flag[0] = True      
        self.camera_processor.start_camera()  # Запуск камери тут
        self.camera_processor.run(self.continue_flag)
       # self.init_ui()

    def close_cam_view(self):
        self.continue_flag[0] = False
        self.camera_processor.close_camera()  # Закриття камери тут


    def cam_ui(self):
        # Додавання нового фрейму для роботи з налаштуваннями камери
        self.frame_camera = tk.Frame(root)
        self.frame_camera.pack(pady=10)

        # Remove buttons for opening and closing camera view
        # self.open_camera_view_button = tk.Button(self.frame_camera, text="Open Camera View", command=self.open_cam_view)
        # self.open_camera_view_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        # self.close_camera_view_button = tk.Button(self.frame_camera, text="Close Camera View", command=self.close_cam_view)
        # self.close_camera_view_button.grid(row=6, column=2, padx=5, pady=5)

        # Кнопка для видалення вибраних налаштувань камери
        self.delete_camera_settings_button = tk.Button(self.frame_camera, text="Delete Selected Settings", command=self.delete_camera_settings)
        self.delete_camera_settings_button.grid(row=5, column=1, padx=5, pady=5)

        # Лейбел для відображення поточних налаштувань
        self.current_settings_label = tk.Label(self.frame_camera, text="Current Settings: None")
        self.current_settings_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Кнопка для завантаження налаштувань з файлу
        self.load_camera_file_button = tk.Button(self.frame_camera, text="Load Settings from File", command=self.load_settings_from_file)
        self.load_camera_file_button.grid(row=5, column=0, padx=5, pady=5)

        # Remove the "Settings Name:" field
        # self.camera_params_label = tk.Label(self.frame_camera, text="Settings Name:")
        # self.camera_params_label.grid(row=0, column=0, padx=5, pady=5)
        # self.camera_params_entry = tk.Entry(self.frame_camera)
        # self.camera_params_entry.grid(row=0, column=1, padx=5, pady=5)

        # Випадаючий список для вибору наявних налаштувань
        self.camera_settings_label = tk.Label(self.frame_camera, text="Select Settings:")
        self.camera_settings_label.grid(row=1, column=0, padx=5, pady=5)
        self.camera_settings_combobox = ttk.Combobox(self.frame_camera, state="readonly")
        self.camera_settings_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.camera_settings_combobox.bind("<<ComboboxSelected>>", self.on_camera_settings_select)

        # Remove buttons for getting and saving settings from/to camera
        # self.get_camera_settings_button = tk.Button(self.frame_camera, text="Get Settings from Camera", command=self.get_camera_settings_from_cam)
        # self.get_camera_settings_button.grid(row=2, column=0, padx=5, pady=5)
        # self.save_camera_settings_button = tk.Button(self.frame_camera, text="Save Current Settings", command=self.save_camera_settings)
        # self.save_camera_settings_button.grid(row=3, column=0, padx=5, pady=5)

        self.set_camera_settings_button = tk.Button(self.frame_camera, text="Apply Settings to Camera", command=self.set_camera_settings_to_cam)
        self.set_camera_settings_button.grid(row=2, column=1, padx=5, pady=5)

    def on_camera_settings_select(self, event):
        """Дії при виборі параметрів камери у списку."""
        selected_name = self.camera_settings_combobox.get()
        saved_settings = load_from_json("camera_settings.json", CameraSettings)
        selected_settings = next((s for s in saved_settings if s.name == selected_name), None)
        if selected_settings:
            messagebox.showinfo("Selected Settings", f"Settings: {selected_settings}")
    
    def update_current_settings_label(self, settings_name):
        """Оновлення лейблу з інформацією про поточні вибрані налаштування."""
        self.current_settings_label.config(text=f"Current Settings: {settings_name}")
        self.current_settings_label.update()

    def delete_camera_settings(self):
        """Видалення вибраних налаштувань камери."""
        try:
            selected_name = self.camera_settings_combobox.get()
            if not selected_name:
                messagebox.showwarning("Warning", "Please select settings to delete.")
                return
            delete_object_from_json("camera_settings.json", CameraSettings, lambda obj: obj.name == selected_name)
            messagebox.showinfo("Success", f"Settings '{selected_name}' deleted!")
            self.load_settings_from_file()  # Перезавантажити список налаштувань після видалення
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete settings: {e}")

    def get_camera_settings_from_cam(self):
        """Зчитуємо параметри з камери."""
        try:
            settings = self.camera_processor.get_settings()  # Потрібно імплементувати у CameraProcessor
            messagebox.showinfo("Camera Settings", f"Current camera settings: {settings}")
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to get settings: {e}")      

    def set_camera_settings_to_cam(self):
        """Передаємо параметри на камеру."""
        try:
            settings_name = self.camera_settings_combobox.get()
            if not settings_name:
                messagebox.showwarning("Warning", "Please select settings to apply.")
                return
            saved_settings = load_from_json("camera_settings.json", CameraSettings)
            selected_settings = next((s for s in saved_settings if s.name == settings_name), None)
            if not selected_settings:
                raise ValueError("Settings not found.")
            self.camera_processor.set_settings(selected_settings)  # Імплементувати у CameraProcessor
            messagebox.showinfo("Success", f"Settings '{settings_name}' applied to the camera.")
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to apply settings: {e}")
    
    def save_camera_settings(self):
        """Зберігаємо параметри камери у файл."""
        try:
            name = self.camera_params_entry.get()
            if not name:
                messagebox.showwarning("Warning", "Please enter a name for the settings.")
                return
            settings = self.camera_processor.get_settings()  # Потрібно імплементувати у CameraProcessor
            camera_settings = CameraSettings(name=name, **settings)
            current_settings = load_from_json("camera_settings.json", CameraSettings)
            current_settings.append(camera_settings)
            save_to_json("camera_settings.json", current_settings)
            messagebox.showinfo("Success", "Camera settings saved successfully!")
            self.load_camera_settings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def load_settings_from_file(self):
        """Завантажуємо налаштування камери у випадаючий список."""
        try:
            saved_settings = load_from_json("camera_settings.json", CameraSettings)
            self.camera_settings_combobox['values'] = [s.name for s in saved_settings]
            if saved_settings:
                self.camera_settings_combobox.set(saved_settings[0].name)
            messagebox.showinfo("Success", "Camera settings loaded successfully!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load settings: Invalid JSON format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotApp(root)
    root.mainloop()
