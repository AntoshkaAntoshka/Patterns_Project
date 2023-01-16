from datetime import date
#from views import Index, About, FlagsList, CreateFlag, CreateCategory, CategoryList, CopyFlag


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

# routes = {
#     '/': Index(),
#     '/about/': About(),
#     '/flags-list/': FlagsList(),
#     '/create-flag/': CreateFlag(),
#     '/create-category/': CreateCategory(),
#     '/category-list/': CategoryList(),
#     '/copy-flag/': CopyFlag()
# }
