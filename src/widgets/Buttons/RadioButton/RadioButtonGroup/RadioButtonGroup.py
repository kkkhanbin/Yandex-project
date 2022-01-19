

class RadioButtonGroup:
    def __init__(self, radio_buttons: list):
        self.radio_buttons = radio_buttons

    def get_radio_buttons(self) -> list:
        return self.radio_buttons

    def update(self, radio_button):
        self.normalize_number_of_checked_buttons(radio_button)

    def normalize_number_of_checked_buttons(self, radio_button):
        for checked_buttons in self.get_checked_buttons():
            if not checked_buttons is radio_button:
                checked_buttons.set_checked(False)

    def get_checked_buttons(self) -> list:
        checked_buttons = []
        for button in self.get_radio_buttons():
            if button.get_checked():
                checked_buttons.append(button)
        return checked_buttons

    def get_checked_button(self):
        return self.get_checked_buttons()[0]

    def add_radio_button(self, radio_button):
        self.get_radio_buttons().append(radio_button)
