from widgets.Layouts.Layout import Layout


class VerticalLayout(Layout):
    def position_widgets(self):
        height = round((self.get_rect().height - self.get_spacing() * (
                len(self.get_widgets()) + 1)) / len(self.get_widgets()))

        for i, widget in enumerate(self.get_widgets()):
            widget.get_rect().height = height
            widget.get_rect().y = (
                self.get_spacing() *
                (i + 1)) + (height * i) + self.get_rect().y

            widget.get_rect().width = \
                self.get_rect().width - self.get_spacing() * 2
            widget.get_rect().x = \
                self.get_rect().x + self.get_spacing()
