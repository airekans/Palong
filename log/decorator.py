"""
This script contains some decorators used to output some log.
"""

def log_on_return_given_value(value):
    import logging
    def decorator_func(func):
        def wrapper_func(*args):
            ret = func(*args)
            if ret == value:
                logging.warning('function %s with args %s returns %s'%(
                        func.__name__, args, str(value)))

            return ret
        return wrapper_func
    return decorator_func
