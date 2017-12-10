__author__ = 'omar'

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]

    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def build_header(request):
    meta = dict(request.META)
    return {
        "HTTP_USER_AGENT": meta.get('HTTP_USER_AGENT'),
        "CONTENT_LENGTH": meta.get('CONTENT_LENGTH'),
        "HTTP_COOKIE": meta.get('HTTP_COOKIE'),
        "CONTENT_TYPE": meta.get('CONTENT_TYPE'),
        "HTTP_ACCEPT_ENCODING": meta.get('HTTP_ACCEPT_ENCODING'),
        "HTTP_CONNECTION": meta.get('HTTP_CONNECTION'),
        "HTTP_HOST": meta.get('HTTP_HOST'),
        "HTTP_REFERER": meta.get('HTTP_REFERER'),
        "HTTP_ACCEPT_LANGUAGE": meta.get('HTTP_ACCEPT_LANGUAGE'),
        "REMOTE_ADDR": get_client_ip(request),
        "REMOTE_HOST": meta.get('REMOTE_HOST'),
        "REQUEST_METHOD": meta.get('REQUEST_METHOD'),
        "SERVER_NAME": meta.get('SERVER_NAME'),
        "REMOTE_USER": meta.get('REMOTE_USER'),
        "SERVER_PORT": meta.get('SERVER_PORT'),
        "HTTP_X_FORWARDED_FOR": meta.get('HTTP_X_FORWARDED_FOR')
    }
