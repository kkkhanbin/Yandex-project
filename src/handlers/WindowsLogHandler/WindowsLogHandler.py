class WindowsLogHandler:
    def __init__(self, objects: list):
        self.objects = objects

    def get(self) -> list:
        return self.objects

    def add(self, objects: list):
        self.objects.append(*objects)
        return self

    def pop(self) -> object:
        return self.objects.pop()
