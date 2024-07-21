from Blog_Project.settings import PAGE_LIMIT
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_paginated_results(data_list, page_number, page_limit=None):
    try:
        if page_limit is None:
            page_limit = PAGE_LIMIT
            
        paginator = Paginator(data_list, page_limit)

        try:
            page_obj = paginator.page(page_number)
            page_list = page_obj.object_list
            if hasattr(page_list, 'query'):
                page_object = f"Query for page: {page_list.query}"
            else:
                page_object = f"Object for page: {page_list}"


        except PageNotAnInteger:
            page_obj = paginator.page(1)
        
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        except Exception as e:
            pass


        page_context = {
            "page_number": page_number,
            "page_count": len(page_obj.object_list),
            "total_count": paginator.count,
            "total_number_of_pages": paginator.num_pages
        }

        return page_obj, page_context

    except Exception as e:
        raise e
