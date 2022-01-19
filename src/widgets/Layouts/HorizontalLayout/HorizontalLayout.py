from widgets.Layouts.Layout import Layout


class HorizontalLayout(Layout):
    def position_widgets(self):
        width = round((self.get_rect().width - self.get_spacing() * (
                len(self.get_widgets()) + 1)) / len(self.get_widgets()))

        for i, widget in enumerate(self.get_widgets()):
            widget.get_rect().width = width
            widget.get_rect().x = (
                self.get_spacing() * (i + 1)) + (width * i) + self.get_rect().x

            widget.get_rect().height = \
                self.get_rect().height - self.get_spacing() * 2
            widget.get_rect().y = \
                self.get_rect().y + self.get_spacing()
