from enum import Enum


class Styles(Enum):
    """
    This class is used to define the styles for the text in the terminal
    """
    bold = '\033[01m'
    italic = '\33[3m'
    end = '\033[0m'
    green = '\33[32m'
    yellow = '\33[33m'
    blue = '\33[34m'
    voilet = '\33[35m'
    beige = '\33[36m'
    red = '\33[31m'
