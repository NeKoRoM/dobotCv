import json
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from save import RobotPosition, CameraSettings, save_to_json, load_from_json, delete_object_from_json
from dobot import DobotController
from camTk import CameraProcessor
import threading
from robotControl import init_robot_ui
from managerTab import init_manager_ui



class RobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Position & Camera Settings Manager")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        self.robot_frame = tk.Frame(self.notebook)
        self.camera_frame = tk.Frame(self.notebook)
        self.manager_frame = tk.Frame(self.notebook)
        self.main_frame = tk.Frame(self.notebook)

        self.notebook.add(self.robot_frame, text="Robot Control")
        self.notebook.add(self.camera_frame, text="Camera Settings")
        self.notebook.add(self.manager_frame, text="Manager")
        self.notebook.add(self.main_frame, text="Main Program")

        init_robot_ui(self.robot_frame)
        self.camera_processor = CameraProcessor(self.camera_frame)
        init_manager_ui(self.manager_frame)
        self.init_main_program_ui(self.main_frame)

        self.continue_flag = [True]  # Ініціалізація атрибута continue_flag
        self.camera_thread = None

        """Ініціалізація підключення до Dobot."""
        try:
            self.dobot_controller = DobotController()
            messagebox.showinfo("Dobot Connected", "Dobot successfully connected.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect Dobot: {e}")
    

    def init_main_program_ui(self, frame):
        tk.Label(frame, text="Pick Position:").grid(row=0, column=0, padx=5, pady=5)
        self.pick_position_combobox = ttk.Combobox(frame, state="readonly")
        self.pick_position_combobox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Place Position:").grid(row=1, column=0, padx=5, pady=5)
        self.place_position_combobox = ttk.Combobox(frame, state="readonly")
        self.place_position_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Product Size (cm):").grid(row=2, column=0, padx=5, pady=5)
        self.product_size_entry = tk.Entry(frame)
        self.product_size_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Camera Settings:").grid(row=3, column=0, padx=5, pady=5)
        self.camera_settings_combobox = ttk.Combobox(frame, state="readonly")
        self.camera_settings_combobox.grid(row=3, column=1, padx=5, pady=5)

        self.load_main_program_data()

    def load_main_program_data(self):
        try:
            robot_positions = load_from_json("robot_positions.json", RobotPosition)
            self.pick_position_combobox['values'] = [pos.name for pos in robot_positions]
            self.place_position_combobox['values'] = [pos.name for pos in robot_positions]

            camera_settings = load_from_json("camera_settings.json", CameraSettings)
            self.camera_settings_combobox['values'] = [settings.name for settings in camera_settings]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotApp(root)
    root.mainloop()
