from constants.level.level_settings import TUPLE_SEPARATOR


class ConvertHandler:
    @staticmethod
    def convert_percent(target_value: tuple, *values):
        """Принимает значение от которого будут конвертироваться значения и
        сами значения в виде коллекций"""
        return tuple(map(lambda value: (
            round(value[0] * target_value[0]),
            round(value[1] * target_value[1])), values))

    @staticmethod
    def str_to_tuple(value: str, convert_type, sep=TUPLE_SEPARATOR):
        return tuple(map(convert_type, value.split(sep)))
