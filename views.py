from datetime import date
from simba_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}


# контроллер "Главная страница"
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', 
                                objects_list=site.categories)



@AppRoute(routes=routes, url='/about/')
# контроллер "О сайте"
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')



# контроллер "404"
class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'



# контроллер "Список флагов"
@AppRoute(routes=routes, url='/flags-list/')
class FlagsList:
    def __call__(self, request):
        logger.log('Список флагов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('flag_list.html', 
                                    objects_list=category.flags, 
                                    name=category.name, id=category.id)
        
        except KeyError:
            return '200 OK', 'No flags have been added yet'



# контроллер "Создать флаг"
@AppRoute(routes=routes, url='/create-flag/')
class CreateFlag:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод POST

            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                flag = site.create_flag('modernflag', name, category)

                flag.observers.append(email_notifier)
                flag.observers.append(sms_notifier)

                site.flags.append(flag)
            
            return '200 OK', render('flag_list.html', objects_list=category.flags, 
                                                    name=category.name, id=category.id)
        
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_flag.html', name=category.name, 
                                                            id=category.id)

            except KeyError:
                return '200 OK', 'No categories have been added yet'



# контроллер "Создать категорию"
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
        def __call__(self, request):

            if request['method'] == 'POST':
                # метод POST

                data = request['data']
                print(data)

                name = data['name']
                name = site.decode_value(name)
                
                category_id = data.get('category_id')
                category = None

                if category_id:
                    category = site.find_category_by_id(int(category_id))
                
                new_category = site.create_category(name, category)
                site.categories.append(new_category)

                return '200 OK', render('index.html', 
                                        objects_list=site.categories)

            else:
                categories = site.categories
                return '200 OK', render('create_category.html', 
                                        categories=categories)



# контроллер "Список категорий"
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)



# контроллер "Копировать флаг"
@AppRoute(routes=routes, url='/copy-flag/')
class CopyFlag:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            previous_flag = site.get_flag(name)

            if previous_flag:
                new_name = f'copy - {name}'
                new_flag = previous_flag.clone()
                new_flag.name = new_name
                site.flags.append(new_flag)

            return '200 OK', render('flag_list.html', 
                                    objects_list=site.flags, 
                                    name=new_flag.category.name)

        except KeyError:
            '200 OK', 'No courses have been added yet'




@AppRoute(routes=routes, url='/reader-user-list/')
class ReaderUserListView(ListView):
    queryset = site.reader_users
    template_name = 'reader_user_list.html'


@AppRoute(routes=routes, url='/create-reader-user/')
class ReaderUserCreateView(CreateView):
    template_name = 'create_reader_user.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('readeruser', name)
        site.reader_users.append(new_obj)



@AppRoute(routes=routes, url='/add-reader-user/')
class AddReaderUserByFlagCreateView(CreateView):
    template_name = 'add_reader_user.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['flags'] = site.flags
        context['reader_users'] = site.reader_users
        return context

    def create_obj(self, data: dict):
        flag_name = data['flag_name']
        flag_name = site.decode_value(flag_name)
        flag = site.get_flag(flag_name)
        reader_user_name = data['reader_user_name']
        reader_user_name = site.decode_value(reader_user_name)
        reader_user = site.get_reader_user(reader_user_name)
        flag.add_reader_user(reader_user)



@AppRoute(routes=routes, url='/api/')
class FlagApi:
    @Debug(name='FlagApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.flags).save()








