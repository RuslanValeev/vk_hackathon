def headers_middleware(get_response):

    def middleware(request):
        response = get_response(request)
        response['X-Frame-Origin'] = "deny"
        return response

    return middleware