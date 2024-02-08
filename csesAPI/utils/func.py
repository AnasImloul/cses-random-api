from time import perf_counter_ns, sleep


def repeat_on_exception(max_retries=3, sleep_time=1, default_return=None, throw_exception=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_retries):

                # TODO: Add test for args and kwargs

                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if throw_exception and i == max_retries - 1:
                        raise e
                    else:
                        sleep(sleep_time)

            return default_return

        return wrapper

    return decorator


def raise_on_exception(exception):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(func.__name__)
                raise exception(e)

        return wrapper

    return decorator


def execution_time(time_unit='seconds'):
    if time_unit in ('seconds', 'second', 's'):
        scale = 1e-9
        time_unit = 'seconds'
    elif time_unit in ('milliseconds', 'millisecond', 'ms'):
        scale = 1e-6
        time_unit = 'milliseconds'
    elif time_unit in ('microseconds', 'microsecond', 'us'):
        scale = 1e-3
        time_unit = 'microseconds'
    elif time_unit in ('nanoseconds', 'nanosecond', 'ns'):
        scale = 1
        time_unit = 'nanoseconds'
    else:
        scale = 1e-9
        time_unit = 'seconds'

    def decorator(func):
        def wrapper(*args, **kwargs):
            start = perf_counter_ns()
            result = func(*args, **kwargs)
            print(f'Execution time: {round((perf_counter_ns() - start) * scale, 2)} {time_unit}')
            return result

        return wrapper

    return decorator


def return_on_exception(default_return=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return default_return

        return wrapper

    return decorator


def async_return_on_exception(default_return=None):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except:
                return default_return

        return wrapper

    return decorator


def singleton(cls):
    __instances = dict()

    def decorator(*args, **kwargs):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kwargs)

        return __instances[cls]

    return decorator
