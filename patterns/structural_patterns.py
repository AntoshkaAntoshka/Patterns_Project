from time import time

# структурный паттерн "Декоратор"
class AppRoute:
    
    def __init__(self, routes, url):
    # Сохраняем значение переданного параметра
        self.routes = routes
        self.url = url

    def __call__(self, cls):
    # Отработка декоратора в момент вызова
        self.routes[self.url] = cls()



class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        # декоратор для замера времени выполнения функции
        def timeit(method):
            def timed(*args, **kwargs):
                start = time()
                result = method(*args, **kwargs)
                end = time()
                delta = end - start

                print(f'debug -----> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed
            
        return timeit(cls)



