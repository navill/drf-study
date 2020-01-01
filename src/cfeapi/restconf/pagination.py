from rest_framework import pagination


class CFEAPIPagination(pagination.LimitOffsetPagination):  # PageNumberPagination):
    # page_size = 2
    default_limit = 10
    max_limit = 20
    limit_query_param = 'lim'
    # offset -> 페이지 넘버 - 1
