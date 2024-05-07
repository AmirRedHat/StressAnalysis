from concurrent.futures import ThreadPoolExecutor
from requests import get


def send(
    request_count: int = 1,
    is_parallel: bool = False,
    workers_count: int = 20,
    *args,
    **kwargs):
    
    def function_decorator(func):
        def class_decorator(class_):
            if is_parallel:
                with ThreadPoolExecutor(max_workers=workers_count) as executor:
                    [executor.submit(func, class_) for _ in range(request_count)]
            else:
                func(class_)
                    
        return class_decorator
    return function_decorator
