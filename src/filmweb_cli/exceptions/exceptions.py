class FilmwebError(Exception):
    pass


class ContentNotFoundError(FilmwebError):
    pass


class InvalidContentError(FilmwebError):
    pass


class InvalidIdTypeException(FilmwebError):
    pass
