class UserNotFoundException(Exception):
    pass


class PasswordMismatchException(Exception):
    pass


class MovieNotFoundException(Exception):
    pass


class InvalidScheduleException(Exception):
    pass


class ScheduleNotFoundException(Exception):
    pass


class ReservationNotFoundException(Exception):
    pass


class ReservationAlreadyExistsException(Exception):
    pass


class SeatNotFoundException(Exception):
    pass
