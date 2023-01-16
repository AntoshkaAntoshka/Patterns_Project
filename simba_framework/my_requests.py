# работа с GET-запросами
class GetRequests:

    @staticmethod
    # получаем строку, парсим её и преобразуем в словарь
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for param in params:
                k, v = param.split('=')
                result[k] = v
        return result # type: dict

    @staticmethod
    def get_request_params(environ):
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # превращаем параметры в словарь
        request_params = GetRequests.parse_input_data(query_string)
        return request_params

# работа с POST-запросами
class PostRequests:

    @staticmethod
    # получаем строку, парсим её и преобразуем в словарь
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for param in params:
                k, v = param.split('=')
                result[k] = v
        return result # type: dict

    @staticmethod
    # получаем данные в байтах
    def get_wsgi_input_data(env) -> bytes:
        # получаем длину тела, она приходит в строковом формате, поэтому формат нужно перевести в int
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int, если тело есть, иначе возвращаем 0
        content_length = int(content_length_data) if content_length_data else 0
        print(content_length)
        # считываем данные если они есть
        data = env['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
        return data # type: bytes

    # получили байты, теперь нужно их декодировать и собрать в словарь
    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # декодируем байты в строку
            data_str = data.decode(encoding='utf-8')
            print(f"Строка после декодирования: {data_str}")
            # данные из строки преобразуем в словарь
            result = self.parse_input_data(data_str)
        return result # type: dict

    def get_request_params(self, environ):
        # получаем данные в байтах
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parse_wsgi_input_data(data)
        return data

