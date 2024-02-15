from pygame import init, Rect
init()


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.name = 'camera'
        self.camera_func = camera_func  # func for movement cam
        self.state = Rect(0, 0, width, height)  # rect of all background(layer)

    def apply(self, target):  # movement all items
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
