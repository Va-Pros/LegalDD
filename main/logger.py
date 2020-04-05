from sys import stderr

def log_get_params(get_view):
    def wrapper(request):
        print("GET request params:", file=stderr)
        for key, value in request.GET.items():
            print(key + ': ' + value, file=stderr)
        return get_view(request)
    
    return wrapper


def log_post_params(post_view):
    def wrapper(request):
        print("POST request params:", file=stderr)
        for key, value in request.POST.items():
            print(key + ': ' + value, file=stderr)
        return post_view(request)
    
    return wrapper