from constants.level.level_settings import TUPLE_SEPARATOR

from handlers.ExceptionHandler.ExceptionHandler import ExceptionHandler


class ConvertHandler:
    @staticmethod
    def convert_percent(target_value: tuple, *values):
        """Принимает значение от которого будут конвертироваться значения и
        сами значения в виде коллекций"""
        try:
            return tuple(map(lambda value: (
                round(value[0] * target_value[0]),
                round(value[1] * target_value[1])), values))
        except IndexError as exception:
            ExceptionHandler().log(exception)
        except ValueError as exception:
            ExceptionHandler().log(exception)
        except TypeError as exception:
            ExceptionHandler().log(exception)

    @staticmethod
    def str_to_tuple(value: str, convert_type, sep=TUPLE_SEPARATOR):
        try:
            return tuple(map(convert_type, value.split(sep)))
        except ValueError as exception:
            ExceptionHandler().log(exception)
        except TypeError as exception:
            ExceptionHandler().log(exception)
