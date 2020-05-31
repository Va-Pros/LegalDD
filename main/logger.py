from sys import stderr

def log_get_params(get_view):
    def wrapper(request, *args, **kwargs):
        print("URL:", request.build_absolute_uri('?'))
        print("GET request params:", file=stderr)
        for key, value in request.GET.items():
            print(key + ': ' + value, file=stderr)
        return get_view(request, *args, **kwargs)
    
    return wrapper


def log_post_params(post_view):
    def wrapper(request, *args, **kwargs):
        print("URL:", request.build_absolute_uri('?'))
        print("POST request params:", file=stderr)
        for key, value in request.POST.items():
            print(key + ': ' + value, file=stderr)
        return post_view(request, *args, **kwargs)
    
    return wrapper