from dobot import DobotController



dobot = DobotController()
device = dobot.device
(x, y, z, r, j1, j2, j3, j4) = dobot.get_current_pos()
device.move_to(x + 20, y, z, r, wait=False)
device.move_to(x, y, z, r, wait=True)  # we wait until this movement is done before continuing