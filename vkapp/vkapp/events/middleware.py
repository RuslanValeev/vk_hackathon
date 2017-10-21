def headers_middleware(get_response):

    def middleware(request):
        response = get_response(request)
        response['X-Frame-Options'] = "deny"
        return response

    return middleware