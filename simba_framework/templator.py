from jinja2 import FileSystemLoader, Template
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Работа с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """

    # создаем объект окружения
    env = Environment()
    # указываем папку, в которой нужно искать шаблоны
    env.loader = FileSystemLoader(folder)
    # находим нужный шаблон
    template = env.get_template(template_name)
    
    return template.render(**kwargs)
