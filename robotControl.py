import json
import tkinter as tk
from tkinter import messagebox, ttk
from save import RobotPosition, load_from_json, save_to_json, delete_object_from_json
from dobot import DobotController

class RobotControl:
    def __init__(self):
        self.dobot_controller = DobotController()

    def init_robot_ui(self, root):
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        name_label = tk.Label(frame_input, text="Position Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(frame_input)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        x_label = tk.Label(frame_input, text="X:")
        x_label.grid(row=1, column=0, padx=5, pady=5)
        x_entry = tk.Entry(frame_input)
        x_entry.grid(row=1, column=1, padx=5, pady=5)

        y_label = tk.Label(frame_input, text="Y:")
        y_label.grid(row=2, column=0, padx=5, pady=5)
        y_entry = tk.Entry(frame_input)
        y_entry.grid(row=2, column=1, padx=5, pady=5)

        z_label = tk.Label(frame_input, text="Z:")
        z_label.grid(row=3, column=0, padx=5, pady=5)
        z_entry = tk.Entry(frame_input)
        z_entry.grid(row=3, column=1, padx=5, pady=5)

        r_label = tk.Label(frame_input, text="R:")
        r_label.grid(row=4, column=0, padx=5, pady=5)
        r_entry = tk.Entry(frame_input)
        r_entry.grid(row=4, column=1, padx=5, pady=5)

        j1_label = tk.Label(frame_input, text="J1:")
        j1_label.grid(row=5, column=0, padx=5, pady=5)
        j1_entry = tk.Entry(frame_input)
        j1_entry.grid(row=5, column=1, padx=5, pady=5)

        j2_label = tk.Label(frame_input, text="J2:")
        j2_label.grid(row=6, column=0, padx=5, pady=5)
        j2_entry = tk.Entry(frame_input)
        j2_entry.grid(row=6, column=1, padx=5, pady=5)

        j3_label = tk.Label(frame_input, text="J3:")
        j3_label.grid(row=7, column=0, padx=5, pady=5)
        j3_entry = tk.Entry(frame_input)
        j3_entry.grid(row=7, column=1, padx=5, pady=5)

        j4_label = tk.Label(frame_input, text="J4:")  # New field for J4
        j4_label.grid(row=8, column=0, padx=5, pady=5)
        j4_entry = tk.Entry(frame_input)
        j4_entry.grid(row=8, column=1, padx=5, pady=5)

        position_label = tk.Label(frame_input, text="Select Position:")
        position_label.grid(row=9, column=0, padx=5, pady=5)
        
        position_combobox = ttk.Combobox(frame_input, state="readonly")
        position_combobox.grid(row=9, column=1, padx=5, pady=5)
        position_combobox.bind("<<ComboboxSelected>>", lambda event: self.on_position_select(event, position_combobox, x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry))

        save_button = tk.Button(frame_buttons, text="Save Position", command=lambda: self.save_position(name_entry, x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry, position_combobox))
        save_button.grid(row=0, column=0, padx=10, pady=10)

        load_button = tk.Button(frame_buttons, text="Load Positions", command=lambda: self.load_positions(position_combobox))
        load_button.grid(row=0, column=1, padx=10, pady=10)

        delete_button = tk.Button(frame_buttons, text="Delete Position", command=lambda: self.delete_position(position_combobox))
        delete_button.grid(row=0, column=2, padx=10, pady=10)

        update_position_button = tk.Button(frame_buttons, text="Update Pos from bot", command=lambda: self.update_robot_position(x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry))
        update_position_button.grid(row=3, column=0, padx=10, pady=10)

        move_button = tk.Button(frame_buttons, text="Move", command=lambda: self.move_robot_to_position(x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry))
        move_button.grid(row=3, column=1, padx=10, pady=10)

        suction_button = tk.Button(frame_buttons, text="Toggle Suction", command=self.toggle_suction)
        suction_button.grid(row=4, column=0, padx=10, pady=10)

        self.load_positions(position_combobox)

    def save_position(self, name_entry, x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry, position_combobox):
        name = name_entry.get()
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            z = float(z_entry.get())
            r = float(r_entry.get())
            j1 = float(j1_entry.get())
            j2 = float(j2_entry.get())
            j3 = float(j3_entry.get())
            j4 = float(j4_entry.get())
            
            robot_pos = RobotPosition(x, y, z, r, j1, j2, j3, j4, name)
            current_positions = load_from_json("robot_positions.json", RobotPosition)
            current_positions.append(robot_pos)
            save_to_json("robot_positions.json", current_positions)
            messagebox.showinfo("Success", "Robot position saved successfully!")
            self.load_positions(position_combobox)
            name_entry.delete(0, tk.END)
            x_entry.delete(0, tk.END)
            y_entry.delete(0, tk.END)
            z_entry.delete(0, tk.END)
            r_entry.delete(0, tk.END)
            j1_entry.delete(0, tk.END)
            j2_entry.delete(0, tk.END)
            j3_entry.delete(0, tk.END)
            j4_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for position.")

    def load_positions(self, position_combobox):
        try:
            robot_positions = load_from_json("robot_positions.json", RobotPosition)
            position_combobox['values'] = [pos.name for pos in robot_positions]
            if robot_positions:
                position_combobox.set(robot_positions[0].name)
            messagebox.showinfo("Success", "Positions loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading positions: {e}")

    def on_position_select(self, event, position_combobox, x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry):
        selected_name = position_combobox.get()
        robot_positions = load_from_json("robot_positions.json", RobotPosition)
        selected_position = next((pos for pos in robot_positions if pos.name == selected_name), None)
        
        if selected_position:
            x_entry.delete(0, tk.END)
            x_entry.insert(0, selected_position.x)

            y_entry.delete(0, tk.END)
            y_entry.insert(0, selected_position.y)

            z_entry.delete(0, tk.END)
            z_entry.insert(0, selected_position.z)

            r_entry.delete(0, tk.END)
            r_entry.insert(0, selected_position.r)

            j1_entry.delete(0, tk.END)
            j1_entry.insert(0, selected_position.j1)

            j2_entry.delete(0, tk.END)
            j2_entry.insert(0, selected_position.j2)

            j3_entry.delete(0, tk.END)
            j3_entry.insert(0, selected_position.j3)

            j4_entry.delete(0, tk.END)
            j4_entry.insert(0, selected_position.j4)

    def delete_position(self, position_combobox):
        name_to_delete = position_combobox.get()
        if not name_to_delete:
            messagebox.showwarning("Warning", "Please select a position to delete.")
            return
        try:
            delete_object_from_json("robot_positions.json", RobotPosition, lambda obj: obj.name == name_to_delete)
            messagebox.showinfo("Success", f"Position with name '{name_to_delete}' deleted!")
            self.load_positions(position_combobox)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the position: {e}")

    def update_robot_position(self, x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry):
        try:
            position = self.dobot_controller.get_current_pos()
            if position:
                x, y, z, r, j1, j2, j3, j4 = position
                x_entry.delete(0, tk.END)
                x_entry.insert(0, f"{x:.2f}")
                y_entry.delete(0, tk.END)
                y_entry.insert(0, f"{y:.2f}")
                z_entry.delete(0, tk.END)
                z_entry.insert(0, f"{z:.2f}")
                r_entry.delete(0, tk.END)
                r_entry.insert(0, f"{r:.2f}")
                j1_entry.delete(0, tk.END)
                j1_entry.insert(0, f"{j1:.2f}")
                j2_entry.delete(0, tk.END)
                j2_entry.insert(0, f"{j2:.2f}")
                j3_entry.delete(0, tk.END)
                j3_entry.insert(0, f"{j3:.2f}")
                j4_entry.delete(0, tk.END)
                j4_entry.insert(0, f"{j4:.2f}")
        except Exception as e:
            messagebox.showerror("Position Error", f"Failed to update position: {e}")

    def move_robot_to_position(self, x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry):
        try:
            x = float(x_entry.get())
            y = float(y_entry.get())
            z = float(z_entry.get())
            r = float(r_entry.get())
            j1 = float(j1_entry.get())
            j2 = float(j2_entry.get())
            j3 = float(j3_entry.get())
            j4 = float(j4_entry.get())
            self.dobot_controller.move_to_custom(x, y, z, r)
            messagebox.showinfo("Movement", f"Robot moved to position: x={x}, y={y}, z={z}, r={r}, j1={j1}, j2={j2}, j3={j3}, j4={j4}")
            self.update_robot_position(x_entry, y_entry, z_entry, r_entry, j1_entry, j2_entry, j3_entry, j4_entry)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for x, y, z, r, j1, j2, j3, and j4.")
        except Exception as e:
            messagebox.showerror("Movement Error", f"Failed to move robot: {e}")

    def toggle_suction(self):
        try:
            state = not getattr(self.dobot_controller, "suction_state", False)
            self.dobot_controller.toggle_suction(state)
            self.dobot_controller.suction_state = state
            status = "enabled" if state else "disabled"
            messagebox.showinfo("Suction", f"Suction cup {status}.")
        except Exception as e:
            messagebox.showerror("Suction Error", f"Failed to toggle suction: {e}")
