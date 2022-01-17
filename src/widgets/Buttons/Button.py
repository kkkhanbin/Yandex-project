from widgets.Widget import Widget


class Button(Widget):
    def is_pos_inside(self, pos: tuple) -> bool:
        return self.get_rect().collidepoint(*pos)
