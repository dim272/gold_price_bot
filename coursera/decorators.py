def decorator(func):
    return func

@decorator
def decorated():
    print('Hello!')

decorated()