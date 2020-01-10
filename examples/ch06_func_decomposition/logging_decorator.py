"""
logging_decorator.py - defines a decorator for logging function arguments and
results

Usage example:
    @log_call
    def my_func(a, b, c):
        ...
"""

import inspect

# stack = inspect.stack()[1][3]


def log_call(log_return_value=False):
    """Decorator for logging function arguments and results"""
    def decorator(fn):
        """Decorator for logging function arguments and results"""
        def log_args_and_results(*args, **kwargs):
            print('{}{}({}){}'.format(
                ' ' * (len(inspect.stack()) * 2),
                fn.__name__,
                format_args(*args, **kwargs),
                ': enter' if log_return_value else ''))

            # call the decorated function
            result = fn(*args, **kwargs)  # unwrap the argument lists

            if log_return_value:
                print('{}({}): exit, result: {}'.format(
                    fn.__name__, format_args(*args, **kwargs), result))
            return result

        # outer function returns reference to nested function
        return log_args_and_results
    return decorator


def format_args(*args, **kwargs):
    """Formats all arguments into a single string"""
    return ", ".join(str(a) for a in args) + \
        (", " + ", ".join(str(k) + '=' + str(v) for k, v in kwargs.items())
            if kwargs else '')
