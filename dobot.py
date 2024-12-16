from serial.tools import list_ports
from pydobot import Dobot

class DobotController:
    def __init__(self):
        """Ініціалізація з'єднання з роботом"""
        self.device = None
        self.connect()

    def connect(self):
        """Підключення до робота"""
        try:
            port = list_ports.comports()[0].device
            self.device = Dobot(port=port, verbose=True)
            print("Підключено до робота.")
            return True
        except Exception as e:
            print(f"Помилка при підключенні: {e}")
            return False

    def get_current_pos(self):
        """Отримання поточної позиції робота"""
        try:
            if self.device:
                (x, y, z, r, j1, j2, j3, j4) = self.device.pose()
                print(f"Поточна позиція: x:{x:.2f} y:{y:.2f} z:{z:.2f} r:{r:.2f}")
                return x, y, z, r, j1, j2, j3,
            else:
                print("Робот не підключений.")
                return None
        except Exception as e:
            print(f"Помилка при отриманні позиції: {e}")
            return None

    def move_to_custom(self, x, y, z, r):
        """Переміщення до заданої позиції"""
        try:
            # Переміщення до нової позиції
            self.device.move_to(x, y, z, r, wait=True)
            print(f"Переміщення до: x:{x} y:{y} z:{z} r:{r}")
            return self.get_current_pos()
        except Exception as e:
            print(f"Помилка при переміщенні: {e}")
            return None

    def toggle_suction(self, state):
        """Включає або вимикає вакуумний насос"""
        try:
            if state:
                self.device._set_end_effector_suction_cup(True)
                print("Вакуумний насос увімкнений.")
            else:
                self.device._set_end_effector_suction_cup(False)
                print("Вакуумний насос вимкнений.")
            return state
        except Exception as e:
            print(f"Помилка при керуванні вакуумом: {e}")
            return None

    def close(self):
        """Закриває з'єднання з роботом"""
        if self.device:
            self.device.close()
            print("З'єднання з роботом закрито.")
            return True
        else:
            print("Робот не підключений.")
            return False

# Використання класу
# controller = DobotController()

# Приклад виклику функцій з параметрами:
# current_pos = controller.move_to_custom(100, 200, 300, 45)  # Переміщення до координат (100, 200, 300, 45)
# print(f"Нова позиція: {current_pos}")

# suction_state = controller.toggle_suction(True)   # Увімкнення вакуумного насоса
# print(f"Стан вакууму: {suction_state}")

# current_pos = controller.get_current_pos()      # Отримання поточної позиції
# print(f"Поточна позиція: {current_pos}")

# is_connected = controller.close()                # Закриття з'єднання з роботом
# print(f"З'єднання закрито: {is_connected}")
