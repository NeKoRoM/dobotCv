import tkinter as tk
from tkinter import messagebox, filedialog
from robot_position import RobotPosition, CameraSettings, save_to_json, load_from_json, delete_object_from_json

class RobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Position & Camera Settings Manager")

        # Віджети для введення даних
        self.name_label = tk.Label(root, text="Position Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.x_label = tk.Label(root, text="X:")
        self.x_label.pack()
        self.x_entry = tk.Entry(root)
        self.x_entry.pack()

        self.y_label = tk.Label(root, text="Y:")
        self.y_label.pack()
        self.y_entry = tk.Entry(root)
        self.y_entry.pack()

        self.z_label = tk.Label(root, text="Z:")
        self.z_label.pack()
        self.z_entry = tk.Entry(root)
        self.z_entry.pack()

        self.r_label = tk.Label(root, text="R:")
        self.r_label.pack()
        self.r_entry = tk.Entry(root)
        self.r_entry.pack()

        self.j1_label = tk.Label(root, text="J1:")
        self.j1_label.pack()
        self.j1_entry = tk.Entry(root)
        self.j1_entry.pack()

        self.j2_label = tk.Label(root, text="J2:")
        self.j2_label.pack()
        self.j2_entry = tk.Entry(root)
        self.j2_entry.pack()

        self.j3_label = tk.Label(root, text="J3:")
        self.j3_label.pack()
        self.j3_entry = tk.Entry(root)
        self.j3_entry.pack()

        self.save_button = tk.Button(root, text="Save Position", command=self.save_position)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Positions", command=self.load_positions)
        self.load_button.pack()

        self.delete_button = tk.Button(root, text="Delete Position by Name", command=self.delete_position)
        self.delete_button.pack()

    def save_position(self):
        # Зберігаємо позицію робота
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
            save_to_json("robot_positions.json", [robot_pos])
            messagebox.showinfo("Success", "Robot position saved successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for position.")

    def load_positions(self):
        # Завантажуємо позиції робота
        try:
            robot_positions = load_from_json("robot_positions.json", RobotPosition)
            for pos in robot_positions:
                print(pos)  # Тут ви можете додати логіку для відображення на інтерфейсі
            messagebox.showinfo("Success", "Positions loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading positions: {e}")

    def delete_position(self):
        # Видалення позиції за назвою
        name_to_delete = self.name_entry.get()
        try:
            delete_object_from_json("robot_positions.json", RobotPosition, lambda obj: obj.name == name_to_delete)
            messagebox.showinfo("Success", f"Position with name '{name_to_delete}' deleted!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the position: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotApp(root)
    root.mainloop()
