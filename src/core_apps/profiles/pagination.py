from rest_framework.pagination import PageNumberPagination

#Set up pagination on per-model basis
class ProfilePagination(PageNumberPagination):
    page_size = 10 #number of objects in each page
    page_size_query_param = "page_size" #specifies name oe of query parameter used to specify page number 
    max_page_size = 20 #specify maximum number of objects to be returned in each page (sets a cap)
    