from widgets.Layouts.Layout import Layout


class VerticalLayout(Layout):
    def position_widgets(self):
        height = round((self.get_rect().height - self.get_spacing() * (
                len(self.get_widgets()) + 1)) / len(self.get_widgets()))
        y = self.get_spacing()

        width = self.get_rect().width - self.get_spacing() * 2
        x = self.get_rect().x + self.get_spacing()

        for i, widget in enumerate(self.get_widgets()):
            widget.get_rect().height = height \
                if height >= widget.get_min_height() \
                else widget.get_min_height()
            widget.get_rect().y = y

            widget.get_rect().width = width \
                if width >= widget.get_min_width() else widget.get_min_width()
            widget.get_rect().x = x

            y += widget.get_rect().height
