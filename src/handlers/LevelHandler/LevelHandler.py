import os
import csv

from constants.paths import LEVELS_PATH, PARAMETERS_PATH
from constants.level.level_settings import STARS_PAR_NAME, OPENED_PAR_NAME, \
    TIME_PAR_NAME, NAME_PAR_NAME, LEVEL_ICON_PATH, DEFAULT_PARAMETERS, \
    PAR_SEPARATOR, UNLOCK_LEVEL_NAME

from handlers.ExceptionHandler.ExceptionHandler import ExceptionHandler


class LevelHandler:
    def get_level_info(self, level_path: str) -> dict:
        """Загружает информацию об уровне"""
        parameters_path = os.path.join(level_path, PARAMETERS_PATH)

        with open(parameters_path,  encoding='utf-8') as parameters_file:
            # Если что-то пошло не так во время читания файла, выполняется
            # normalize_level_parameters
            try:
                parameters = self.get_parameters(parameters_file)
            except IndexError:
                self.normalize_level_parameters(level_path)
                parameters = self.get_parameters(parameters_file)

            try:
                return self.get_parameters_dict(parameters)
            except KeyError:
                self.normalize_level_parameters(level_path)
                return self.get_parameters_dict(parameters)

    def get_parameters(self, parameters_file) -> dict:
        reader = csv.DictReader(
            parameters_file, delimiter=PAR_SEPARATOR)
        return list(reader)[0]

    def get_parameters_dict(self, parameters: dict) -> dict:
        try:
            stars = int(parameters[STARS_PAR_NAME])
            time = float(parameters[TIME_PAR_NAME])
            opened = True if parameters[OPENED_PAR_NAME] == 'True' \
                else False
            name = parameters[NAME_PAR_NAME]
            unlock_level = parameters[UNLOCK_LEVEL_NAME]

            return {STARS_PAR_NAME: stars, TIME_PAR_NAME: time,
                    OPENED_PAR_NAME: opened, NAME_PAR_NAME: name,
                    UNLOCK_LEVEL_NAME: unlock_level}
        except ValueError as exception:
            ExceptionHandler().log(exception)

    def normalize_level_parameters(self, level_path: str):
        """Заполняет колонки в csv файле"""
        with open(os.path.join(level_path, PARAMETERS_PATH),
                  encoding='utf-8', mode='w') as parameters_file:
            writer = csv.writer(parameters_file, delimiter=PAR_SEPARATOR)
            writer.writerows(DEFAULT_PARAMETERS)
