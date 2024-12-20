import json

class CameraSettings:
    def __init__(self, name, exposure, focus, hsv_lower, hsv_upper):
        self.name = name
        self.exposure = exposure
        self.focus = focus
        self.hsv_lower = hsv_lower
        self.hsv_upper = hsv_upper

    def __str__(self):
        return (f"CameraSettings(name={self.name}, exposure={self.exposure}, "
                f"focus={self.focus}, hsv_lower={self.hsv_lower}, hsv_upper={self.hsv_upper})")

    def to_dict(self):
        return {
            "name": self.name,
            "exposure": self.exposure,
            "focus": self.focus,
            "hsv_lower": self.hsv_lower,
            "hsv_upper": self.hsv_upper
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            exposure=data["exposure"],
            focus=data["focus"],
            hsv_lower=data["hsv_lower"],
            hsv_upper=data["hsv_upper"]
        )

    def save(self, filename):
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file, indent=4)


class RobotPosition:
    def __init__(self, x, y, z, r, j1, j2, j3, name):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.j1 = j1
        self.j2 = j2
        self.j3 = j3
        self.name = name

    def __str__(self):
        return (f"RobotPosition(name={self.name}, "
                f"x={self.x}, y={self.y}, z={self.z}, r={self.r}, "
                f"j1={self.j1}, j2={self.j2}, j3={self.j3})")

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "r": self.r,
            "j1": self.j1,
            "j2": self.j2,
            "j3": self.j3,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            x=data["x"],
            y=data["y"],
            z=data["z"],
            r=data["r"],
            j1=data["j1"],
            j2=data["j2"],
            j3=data["j3"],
            name=data["name"]
        )

# Функція для збереження об'єктів у JSON
def save_to_json(filename, data):
    with open(filename, "w") as file:
        json.dump([obj.to_dict() for obj in data], file, indent=4)

# Функція для зчитування об'єктів з JSON файлу
def load_from_json(filename, class_type):
    with open(filename, "r") as file:
        data = json.load(file)
        if isinstance(data, list):
            return [class_type.from_dict(item) for item in data]
        else:
            return [class_type.from_dict(data)]

# Функція для видалення об'єкта за умовою (наприклад, за назвою)
def delete_object_from_json(filename, class_type, delete_criteria):
    objects = load_from_json(filename, class_type)
    updated_objects = [obj for obj in objects if not delete_criteria(obj)]
    save_to_json(filename, updated_objects)

# Приклад критерію для видалення (видалити за назвою)
def delete_by_name(obj, name):
    return obj.name == name

# Створення об'єктів для збереження
camera1 = CameraSettings("Camera1", 0.01, 1.5, [35, 100, 100], [85, 255, 255])
camera2 = CameraSettings("Camera2", 0.02, 2.0, [40, 120, 110], [80, 255, 255])
robot_pos1 = RobotPosition(100, 200, 50, 90, 45, 30, 60, "HomePosition")
robot_pos2 = RobotPosition(150, 250, 100, 45, 60, 45, 30, "PickPosition")

