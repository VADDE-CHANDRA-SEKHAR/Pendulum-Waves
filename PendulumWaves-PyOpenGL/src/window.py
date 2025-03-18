import glfw

class Window:
    def __init__(self, width, height, title):
        if not glfw.init():
            print("Unable to initialize GLFW")
            return

        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(width, height, title, None, None)
        if (self.window == None):
            print("Unable to create a window")
            return

        glfw.set_window_size_callback(self.window, self._on_window_resize)
        glfw.make_context_current(self.window)

        self.current_time = glfw.get_time()
        self.last_time = 0
        self.last_delta_time = 0.
        self.delta_time = self.current_time - self.last_time
        self.resized = False

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def poll_events(self) -> None:
        self.resized = False
        glfw.poll_events()

    def update_time(self):
        self.last_time = self.current_time
        self.current_time = glfw.get_time()
        self.last_delta_time = self.delta_time
        self.delta_time = self.current_time - self.last_time

    def incremental_update_time(self):
        self.current_time = glfw.get_time()
        self.delta_time = self.current_time - self.last_time

    def is_key_pressed(self, glfw_key_code: int) -> bool:
        return glfw.get_key(self.window, glfw_key_code)

    def is_mouse_button_pressed(self, glfw_mouse_button_code: int) -> bool:
        return glfw.get_mouse_button(self.window, glfw_mouse_button_code)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def get_window_size(self) -> tuple[int, int]:
        return glfw.get_window_size(self.window, )

    def _on_window_resize(self, window, w, h) -> None:
        self.resized = True

