import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from save import RobotPosition, CameraSettings, save_to_json, load_from_json, delete_object_from_json
from dobot import DobotController
from cam import CameraProcessor
import threading



class RobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Position & Camera Settings Manager")


        """Ініціалізація підключення до Dobot."""
        try:
            self.dobot_controller = DobotController()
            messagebox.showinfo("Dobot Connected", "Dobot successfully connected.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect Dobot: {e}") 

        self.camera_processor = CameraProcessor()
        self.init_ui()
        self.continue_flag = [True]  # Ініціалізація атрибута continue_flag
        self.open_cam_view()
        self.close_cam_view()


    def init_ui(self):
        self.cam_ui()    
        # Створення фреймів для групування віджетів
        self.frame_input = tk.Frame(root)
        self.frame_input.pack(pady=10)

        self.frame_buttons = tk.Frame(root)
        self.frame_buttons.pack(pady=10)

        # Введення даних для нової позиції робота
        self.name_label = tk.Label(self.frame_input, text="Position Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.frame_input)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.x_label = tk.Label(self.frame_input, text="X:")
        self.x_label.grid(row=1, column=0, padx=5, pady=5)
        self.x_entry = tk.Entry(self.frame_input)
        self.x_entry.grid(row=1, column=1, padx=5, pady=5)

        self.y_label = tk.Label(self.frame_input, text="Y:")
        self.y_label.grid(row=2, column=0, padx=5, pady=5)
        self.y_entry = tk.Entry(self.frame_input)
        self.y_entry.grid(row=2, column=1, padx=5, pady=5)

        self.z_label = tk.Label(self.frame_input, text="Z:")
        self.z_label.grid(row=3, column=0, padx=5, pady=5)
        self.z_entry = tk.Entry(self.frame_input)
        self.z_entry.grid(row=3, column=1, padx=5, pady=5)

        self.r_label = tk.Label(self.frame_input, text="R:")
        self.r_label.grid(row=4, column=0, padx=5, pady=5)
        self.r_entry = tk.Entry(self.frame_input)
        self.r_entry.grid(row=4, column=1, padx=5, pady=5)

        self.j1_label = tk.Label(self.frame_input, text="J1:")
        self.j1_label.grid(row=5, column=0, padx=5, pady=5)
        self.j1_entry = tk.Entry(self.frame_input)
        self.j1_entry.grid(row=5, column=1, padx=5, pady=5)

        self.j2_label = tk.Label(self.frame_input, text="J2:")
        self.j2_label.grid(row=6, column=0, padx=5, pady=5)
        self.j2_entry = tk.Entry(self.frame_input)
        self.j2_entry.grid(row=6, column=1, padx=5, pady=5)

        self.j3_label = tk.Label(self.frame_input, text="J3:")
        self.j3_label.grid(row=7, column=0, padx=5, pady=5)
        self.j3_entry = tk.Entry(self.frame_input)
        self.j3_entry.grid(row=7, column=1, padx=5, pady=5)

        # Випадаючий список для вибору наявних позицій
        self.position_label = tk.Label(self.frame_input, text="Select Position:")
        self.position_label.grid(row=8, column=0, padx=5, pady=5)
        
        self.position_combobox = ttk.Combobox(self.frame_input, state="readonly")
        self.position_combobox.grid(row=8, column=1, padx=5, pady=5)
        self.position_combobox.bind("<<ComboboxSelected>>", self.on_position_select)

        # Кнопки для збереження, завантаження та видалення позицій
        self.save_button = tk.Button(self.frame_buttons, text="Save Position", command=self.save_position)
        self.save_button.grid(row=0, column=0, padx=10, pady=10)

        self.load_button = tk.Button(self.frame_buttons, text="Load Positions", command=self.load_positions)
        self.load_button.grid(row=0, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.frame_buttons, text="Delete Position", command=self.delete_position)
        self.delete_button.grid(row=0, column=2, padx=10, pady=10)

        """Додавання кнопок для керування роботом."""
        self.update_position_button = tk.Button(self.frame_buttons, text="Update Pos from bot", command=self.update_robot_position)
        self.update_position_button.grid(row=3, column=0, padx=10, pady=10)

        self.move_button = tk.Button(self.frame_buttons, text="Move", command=self.move_robot_to_position)
        self.move_button.grid(row=3, column=1, padx=10, pady=10)

        self.suction_button = tk.Button(self.frame_buttons, text="Toggle Suction", command=self.toggle_suction)
        self.suction_button.grid(row=4, column=0, padx=10, pady=10)

        # Завантажити позиції при запуску програми
        self.load_positions()



        
    def open_cam_view(self):
        self.continue_flag[0] = True      
        self.camera_thread = threading.Thread(target=self.camera_processor.run, daemon=True, args=(continue_flag,))
        self.camera_thread.start()
       # self.init_ui()

    def close_cam_view(self):
        self.continue_flag[0] = False
        self.camera_thread.join()

    def cam_ui(self):


        # Додавання нового фрейму для роботи з налаштуваннями камери
        self.frame_camera = tk.Frame(root)
        self.frame_camera.pack(pady=10)

        # Кнопка для відкриття перегляду камери
        self.open_camera_view_button = tk.Button(self.frame_camera, text="Open Camera View", command=self.open_cam_view)
        self.open_camera_view_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        # Кнопка для закриття перегляду камери
        self.close_camera_view_button = tk.Button(self.frame_camera, text="Close Camera View", command=self.close_cam_view)
        self.close_camera_view_button.grid(row=6, column=2, padx=5, pady=5)

                # Кнопка для видалення вибраних налаштувань камери
        self.delete_camera_settings_button = tk.Button(self.frame_camera, text="Delete Selected Settings", command=self.delete_camera_settings)
        self.delete_camera_settings_button.grid(row=5, column=1, padx=5, pady=5)

        # Лейбел для відображення поточних налаштувань
        self.current_settings_label = tk.Label(self.frame_camera, text="Current Settings: None")
        self.current_settings_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Кнопка для завантаження налаштувань з файлу
        self.load_camera_file_button = tk.Button(self.frame_camera, text="Load Settings from File", command=self.load_settings_from_file)
        self.load_camera_file_button.grid(row=5, column=0, padx=5, pady=5)

        # Поле для назви параметрів камери
        self.camera_params_label = tk.Label(self.frame_camera, text="Settings Name:")
        self.camera_params_label.grid(row=0, column=0, padx=5, pady=5)
        self.camera_params_entry = tk.Entry(self.frame_camera)
        self.camera_params_entry.grid(row=0, column=1, padx=5, pady=5)

        # Випадаючий список для вибору наявних налаштувань
        self.camera_settings_label = tk.Label(self.frame_camera, text="Select Settings:")
        self.camera_settings_label.grid(row=1, column=0, padx=5, pady=5)
        self.camera_settings_combobox = ttk.Combobox(self.frame_camera, state="readonly")
        self.camera_settings_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.camera_settings_combobox.bind("<<ComboboxSelected>>", self.on_camera_settings_select)

        # Кнопки для роботи з налаштуваннями камери
        self.get_camera_settings_button = tk.Button(self.frame_camera, text="Get Settings from Camera", command=self.get_camera_settings_from_cam)
        self.get_camera_settings_button.grid(row=2, column=0, padx=5, pady=5)

        self.set_camera_settings_button = tk.Button(self.frame_camera, text="Apply Settings to Camera", command=self.set_camera_settings_to_cam)
        self.set_camera_settings_button.grid(row=2, column=1, padx=5, pady=5)

        self.save_camera_settings_button = tk.Button(self.frame_camera, text="Save Current Settings", command=self.save_camera_settings)
        self.save_camera_settings_button.grid(row=3, column=0, padx=5, pady=5)

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
        return

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
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {e}")

    def save_position(self):
        # Зберігаємо нову позицію робота
        name = self.name_entry.get()
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            z = float(self.z_entry.get())
            r = float(self.r_entry.get())
            j1 = float(self.j1_entry.get())
            j2 = float(self.j2_entry.get())
            j3 = float(self.j3_entry.get())
            
            robot_pos = RobotPosition(x, y, z, r, j1, j2, j3, name)
            current_positions = load_from_json("robot_positions.json", RobotPosition)
            current_positions.append(robot_pos)
            save_to_json("robot_positions.json", current_positions)
            messagebox.showinfo("Success", "Robot position saved successfully!")
            self.load_positions()  # Перезавантажити позиції у випадаючий список
            self.name_entry.delete(0, tk.END)
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
            self.z_entry.delete(0, tk.END)
            self.r_entry.delete(0, tk.END)
            self.j1_entry.delete(0, tk.END)
            self.j2_entry.delete(0, tk.END)
            self.j3_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for position.")

    def load_positions(self):
        # Завантажуємо позиції робота в випадаючий список
        try:
            robot_positions = load_from_json("robot_positions.json", RobotPosition)
            self.position_combobox['values'] = [pos.name for pos in robot_positions]
            if robot_positions:
                self.position_combobox.set(robot_positions[0].name)
            messagebox.showinfo("Success", "Positions loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading positions: {e}")

    def on_position_select(self, event):
        # Автозаповнення полів при виборі позиції
        selected_name = self.position_combobox.get()
        robot_positions = load_from_json("robot_positions.json", RobotPosition)
        selected_position = next((pos for pos in robot_positions if pos.name == selected_name), None)
        
        if selected_position:
            self.x_entry.delete(0, tk.END)
            self.x_entry.insert(0, selected_position.x)

            self.y_entry.delete(0, tk.END)
            self.y_entry.insert(0, selected_position.y)

            self.z_entry.delete(0, tk.END)
            self.z_entry.insert(0, selected_position.z)

            self.r_entry.delete(0, tk.END)
            self.r_entry.insert(0, selected_position.r)

            self.j1_entry.delete(0, tk.END)
            self.j1_entry.insert(0, selected_position.j1)

            self.j2_entry.delete(0, tk.END)
            self.j2_entry.insert(0, selected_position.j2)

            self.j3_entry.delete(0, tk.END)
            self.j3_entry.insert(0, selected_position.j3)

    def delete_position(self):
        # Видалення позиції за назвою
        name_to_delete = self.position_combobox.get()
        if not name_to_delete:
            messagebox.showwarning("Warning", "Please select a position to delete.")
            return
        try:
            delete_object_from_json("robot_positions.json", RobotPosition, lambda obj: obj.name == name_to_delete)
            messagebox.showinfo("Success", f"Position with name '{name_to_delete}' deleted!")
            self.load_positions()  # Перезавантажити список позицій після видалення
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the position: {e}")

    def update_robot_position(self):
        """Оновлення поточної позиції робота в інтерфейсі."""
        try:
            position = self.dobot_controller.get_current_pos()
            if position:
                x, y, z, r, *_ = position
                self.x_entry.delete(0, tk.END)
                self.x_entry.insert(0, f"{x:.2f}")
                self.y_entry.delete(0, tk.END)
                self.y_entry.insert(0, f"{y:.2f}")
                self.z_entry.delete(0, tk.END)
                self.z_entry.insert(0, f"{z:.2f}")
                self.r_entry.delete(0, tk.END)
                self.r_entry.insert(0, f"{r:.2f}")
        except Exception as e:
            messagebox.showerror("Position Error", f"Failed to update position: {e}")

    def move_robot_to_position(self):
        """Переміщення робота до заданої позиції."""
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            z = float(self.z_entry.get())
            r = float(self.r_entry.get())
            self.dobot_controller.move_to_custom(x, y, z, r)
            messagebox.showinfo("Movement", f"Robot moved to position: x={x}, y={y}, z={z}, r={r}")
            self.update_robot_position()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for x, y, z, and r.")
        except Exception as e:
            messagebox.showerror("Movement Error", f"Failed to move robot: {e}")

    def toggle_suction(self):
        """Увімкнення/вимкнення вакуумного насоса."""
        try:
            state = not getattr(self, "suction_state", False)
            self.dobot_controller.toggle_suction(state)
            self.suction_state = state
            status = "enabled" if state else "disabled"
            messagebox.showinfo("Suction", f"Suction cup {status}.")
        except Exception as e:
            messagebox.showerror("Suction Error", f"Failed to toggle suction: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotApp(root)
    root.mainloop()
