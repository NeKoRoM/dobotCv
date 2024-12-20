import tkinter as tk
from tkinter import ttk, messagebox
from save import load_from_json, delete_object_from_json, RobotPosition, CameraSettings

def init_manager_ui(root):
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Frame for Robot Positions
    frame_positions = tk.LabelFrame(frame, text="Robot Positions")
    frame_positions.pack(fill="both", expand=True, padx=10, pady=10)

    position_combobox = ttk.Combobox(frame_positions, state="readonly")
    position_combobox.pack(padx=5, pady=5)
    load_positions(position_combobox)

    delete_position_button = tk.Button(frame_positions, text="Delete Position", command=lambda: delete_position(position_combobox))
    delete_position_button.pack(padx=5, pady=5)

    load_positions_button = tk.Button(frame_positions, text="Load Positions from File", command=lambda: load_positions(position_combobox))
    load_positions_button.pack(padx=5, pady=5)

    # Frame for Camera Settings
    frame_camera_settings = tk.LabelFrame(frame, text="Camera Settings")
    frame_camera_settings.pack(fill="both", expand=True, padx=10, pady=10)

    camera_settings_combobox = ttk.Combobox(frame_camera_settings, state="readonly")
    camera_settings_combobox.pack(padx=5, pady=5)
    load_camera_settings(camera_settings_combobox)

    delete_camera_settings_button = tk.Button(frame_camera_settings, text="Delete Camera Settings", command=lambda: delete_camera_settings(camera_settings_combobox))
    delete_camera_settings_button.pack(padx=5, pady=5)

    load_camera_settings_button = tk.Button(frame_camera_settings, text="Load Camera Settings from File", command=lambda: load_camera_settings(camera_settings_combobox))
    load_camera_settings_button.pack(padx=5, pady=5)

def load_positions(position_combobox):
    try:
        robot_positions = load_from_json("robot_positions.json", RobotPosition)
        position_combobox['values'] = [pos.name for pos in robot_positions]
        if robot_positions:
            position_combobox.set(robot_positions[0].name)
        messagebox.showinfo("Success", "Positions loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading positions: {e}")

def delete_position(position_combobox):
    name_to_delete = position_combobox.get()
    if not name_to_delete:
        messagebox.showwarning("Warning", "Please select a position to delete.")
        return
    try:
        delete_object_from_json("robot_positions.json", RobotPosition, lambda obj: obj.name == name_to_delete)
        messagebox.showinfo("Success", f"Position with name '{name_to_delete}' deleted!")
        load_positions(position_combobox)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting the position: {e}")

def load_camera_settings(camera_settings_combobox):
    try:
        camera_settings = load_from_json("camera_settings.json", CameraSettings)
        camera_settings_combobox['values'] = [s.name for s in camera_settings]
        if camera_settings:
            camera_settings_combobox.set(camera_settings[0].name)
        messagebox.showinfo("Success", "Camera settings loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading camera settings: {e}")

def delete_camera_settings(camera_settings_combobox):
    name_to_delete = camera_settings_combobox.get()
    if not name_to_delete:
        messagebox.showwarning("Warning", "Please select camera settings to delete.")
        return
    try:
        delete_object_from_json("camera_settings.json", CameraSettings, lambda obj: obj.name == name_to_delete)
        messagebox.showinfo("Success", f"Camera settings with name '{name_to_delete}' deleted!")
        load_camera_settings(camera_settings_combobox)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting the camera settings: {e}")
