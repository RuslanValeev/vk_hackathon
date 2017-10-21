def headers_middleware(get_response):

    def middleware(request):
        response = get_response(request)
        response['X-Frame-Options'] = 'ALLOW-FROM https://api.vk.com/'
        return response

    return middleware