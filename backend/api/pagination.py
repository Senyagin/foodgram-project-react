from rest_framework.pagination import PageNumberPagination


class LimitPagePagination(PageNumberPagination):
    """Пагинатор"""
    page_size = 6
    page_size_query_param = 'limit'
