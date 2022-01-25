class ConvertHandler:
    @staticmethod
    def convert_percent(target_value, *values):
        """Принимает значение от которого будут конвертироваться значения и
        сами значения в виде коллекций"""
        return tuple(map(lambda value: (
            round(value[0] * target_value[0]),
            round(value[1] * target_value[1])), values))
