import inspect
from server.settings import SERVER_LOGGER


def log(func):
    def wrapper(*args, **kwargs):
        func_res = func(*args, **kwargs)
        func_name = func.__name__
        calling_from = inspect.stack()[1].function
        msg = f'Функция {func_name}() вызвана из {calling_from}. Аргументы: {args, kwargs}'
        SERVER_LOGGER.debug(msg=msg)
        return func_res
    return wrapper

