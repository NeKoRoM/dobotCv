import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from save import RobotPosition, CameraSettings, save_to_json, load_from_json, delete_object_from_json

class RobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Position & Camera Settings Manager")
        
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

        # Кнопки для збереження, завантаження та видалення позицій
        self.save_button = tk.Button(self.frame_buttons, text="Save Position", command=self.save_position)
        self.save_button.grid(row=0, column=0, padx=10, pady=10)

        self.load_button = tk.Button(self.frame_buttons, text="Load Positions", command=self.load_positions)
        self.load_button.grid(row=0, column=1, padx=10, pady=10)

        self.delete_button = tk.Button(self.frame_buttons, text="Delete Position", command=self.delete_position)
        self.delete_button.grid(row=0, column=2, padx=10, pady=10)

        # Завантажити позиції при запуску програми
        self.load_positions()

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


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotApp(root)
    root.mainloop()
