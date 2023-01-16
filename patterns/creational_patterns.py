from copy import deepcopy
from quopri import decodestring
from .behavioral_patterns import FileWriter, Subject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# редактор
class EditorUser(User):
    pass


# обычный пользователь
class ReaderUser(User):
    def __init__(self, name):
        self.flags = []
        super().__init__(name)


class UserFactory:
    types = {
        'editoruser': EditorUser,
        'readeruser': ReaderUser
    }

    # реализуем порождающий паттерн 'Фабричный метод'
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн 'Прототип'
class FlagPrototype:
    # прототип флага (пример использования: старые флаги, флаги субъектов страны)

    def clone(self):
        return deepcopy(self)


class Flag(FlagPrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.flags.append(self)
        self.reader_users = []
        super().__init__()
    
    def __getitem__(self, item):
        return self.reader_users[item]

    def add_reader_user(self, reader_user: ReaderUser):
        self.reader_users.append(reader_user)
        reader_user.flags.append(self)
        self.notify()

    
# современная версия флага
class ModernFlag(Flag):
    pass


# старая версия флага
class OldFlag(Flag):
    pass


# флаги субъектов страны
class CountrySubjectFlag(Flag):
    pass


class FlagFactory:
    types = {
        'modernflag': ModernFlag,
        'oldflag': OldFlag,
        'countrysubjectflag': CountrySubjectFlag
    }

    # тоже используем 'Фабричный метод'
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# категория
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.flags = []

    def flag_count(self):
        result = len(self.flags)
        if self.category:
            result += self.category.flag_count()
        return result


# основной интерфейс проекта
class Engine:
    
    def __init__(self):
        self.editor_users = []
        self.reader_users = []
        self.flags = []
        self.categories = []


    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)


    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)


    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')


    @staticmethod
    def create_flag(type_, name, category):
        return FlagFactory.create(type_, name, category)

    def get_flag(self, name):
        for item in self.flags:
            if item.name == name:
                return item
        return None

    def get_reader_user(self, name) -> ReaderUser:
        for item in self.reader_users:
            if item.name == name:
                return item


    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн 'Синглтон'
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']
        
        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]

    
class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer


    def log(self, text):
        text = f'log---> {text}'
        # print('log--->', text)
        self.writer.write(text)
