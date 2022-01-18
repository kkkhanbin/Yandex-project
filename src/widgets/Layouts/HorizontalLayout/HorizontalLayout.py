from widgets.Layouts.Layout import Layout


class HorizontalLayout(Layout):
    def position_widgets(self):
        # Ширина отступов
        width = self.get_spacing() * (len(self.get_widgets()) + 1)

        # Ширина виджетов
        for widget in self.get_widgets():
            width += widget.get_rect().width

        # Во сколько раз предпологаемая ширина больше ширины лэйаута
        coeff = width / self.get_rect().width

        for widget in self.get_widgets():
            values_to_convert = \
                [widget.get_rect().width, widget.get_rect().height,
                 widget.get_rect().x, widget.get_rect().y]

            for i in range(len(values_to_convert)):
                values_to_convert[i] = round(values_to_convert[i] * coeff)
