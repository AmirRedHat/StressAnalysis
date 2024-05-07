from concurrent.futures import ThreadPoolExecutor
from requests import get


def send(*args, **kwargs):
    request_count = kwargs.pop("request_count", 1)
    is_parallel = kwargs.pop("is_parallel", False)
    workers_count = kwargs.pop("workers_count", 20)
    
    def function_decorator(func):
        def class_decorator(class_):
            if is_parallel:
                with ThreadPoolExecutor(max_workers=workers_count) as executor:
                    [executor.submit(func, class_) for _ in range(request_count)]
            else:
                func(class_)
                    
        return class_decorator
    return function_decorator


def send_parallel(url: str):
    count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(1000):
            executor.submit(get, url) 
            count += 1
            
    print(count)