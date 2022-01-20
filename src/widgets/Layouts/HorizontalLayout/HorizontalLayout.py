from widgets.Layouts.Layout import Layout


class HorizontalLayout(Layout):
    def position_widgets(self):
        width = round((self.get_rect().width - self.get_spacing() * (
                len(self.get_widgets()) + 1)) / len(self.get_widgets()))
        x = self.get_spacing()

        height = self.get_rect().height - self.get_spacing() * 2
        y = self.get_rect().y + self.get_spacing()

        for i, widget in enumerate(self.get_widgets()):
            widget.get_rect().width = width \
                if width >= widget.get_min_width() else widget.get_min_width()
            widget.get_rect().x = x

            widget.get_rect().height = height \
                if height >= widget.get_min_height() \
                else widget.get_min_height()
            widget.get_rect().y = y

            x += widget.get_rect().width + self.get_spacing()
