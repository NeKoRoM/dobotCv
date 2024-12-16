
class CameraSettings:
    def __init__(self, exposure, focus, hsv_lower, hsv_upper):
        self.exposure = exposure  # Параметр експозиції (наприклад, час експозиції)
        self.focus = focus        # Параметр фокусу (наприклад, відстань до об'єкта)
        self.hsv_lower = hsv_lower  # Нижній межа HSV (потрібен формат [H, S, V])
        self.hsv_upper = hsv_upper  # Верхній межа HSV (потрібен формат [H, S, V])

    def __str__(self):
        return f"CameraSettings(exposure={self.exposure}, focus={self.focus}, hsv_lower={self.hsv_lower}, hsv_upper={self.hsv_upper})"

    def update_exposure(self, new_exposure):
        self.exposure = new_exposure

    def update_focus(self, new_focus):
        self.focus = new_focus

    def update_hsv(self, new_hsv_lower, new_hsv_upper):
        self.hsv_lower = new_hsv_lower
        self.hsv_upper = new_hsv_upper

    def get_exposure(self):
        return self.exposure

    def get_focus(self):
        return self.focus

    def get_hsv(self):
        return self.hsv_lower, self.hsv_upper

# Створення об'єкта класу CameraSettings
camera = CameraSettings(
    exposure=0.01,          # Приклад значення експозиції (час експозиції 10 мс)
    focus=1.5,              # Приклад значення фокусу (відстань 1.5 м)
    hsv_lower=[35, 100, 100],  # Нижній межа HSV (наприклад, [H=35, S=100, V=100])
    hsv_upper=[85, 255, 255]   # Верхній межа HSV (наприклад, [H=85, S=255, V=255])
)

class RobotPosition:
    def __init__(self, x, y, z, r, j1, j2, j3, name):
        self.x = x      # Координата X
        self.y = y      # Координата Y
        self.z = z      # Координата Z
        self.r = r      # Кут обертання (rotation)
        self.j1 = j1    # Кут першого суглоба (joint 1)
        self.j2 = j2    # Кут другого суглоба (joint 2)
        self.j3 = j3    # Кут третього суглоба (joint 3)
        self.name = name  # Назва позиції

    def __str__(self):
        return (f"RobotPosition(name={self.name}, "
                f"x={self.x}, y={self.y}, z={self.z}, r={self.r}, "
                f"j1={self.j1}, j2={self.j2}, j3={self.j3})")

    def update_position(self, x=None, y=None, z=None, r=None, j1=None, j2=None, j3=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z
        if r is not None:
            self.r = r
        if j1 is not None:
            self.j1 = j1
        if j2 is not None:
            self.j2 = j2
        if j3 is not None:
            self.j3 = j3

    def get_position(self):
        return (self.x, self.y, self.z, self.r, self.j1, self.j2, self.j3)

# Створення об'єкта позиції робота
robot_position = RobotPosition(
    x=100, y=200, z=50, r=90, j1=45, j2=30, j3=60, name="HomePosition"
)

# Виведення поточної позиції робота
print(robot_position)

# Оновлення позиції
robot_position.update_position(x=150, y=250, z=100, j1=60, j2=45)

# Виведення оновленої позиції
print("\nUpdated Robot Position:")
print(robot_position)
