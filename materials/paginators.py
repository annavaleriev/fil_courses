from rest_framework.pagination import PageNumberPagination


class LessonAndCoursePagination(PageNumberPagination):
    """ Класс пагинации для уроков и курсов """

    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр запроса для изменения количества элементов на странице
    max_page_size = 100  # Максимальное количество элементов на странице
