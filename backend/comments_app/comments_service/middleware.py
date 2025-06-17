from comments_app.authenticate import CookieJWTAuthentication

class StrawberryJWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.path != '/graphql/':
            response = self.get_response(request)
            return response
        else:
            user = CookieJWTAuthentication().authenticate(request)
            if user:
                request.user = user
            print(f'User: {user}')
        print("Before view execution")
        # print(f'Request user: {request.user}')
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        print("After view execution")
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(f"Processing view: {view_func.__name__}")
        return None  # Or return an HttpResponse to short-circuit

    def process_exception(self, request, exception):
        print(f"Exception caught: {exception}")
        return None  # Or return an HttpResponse to handle the exception

    def process_response(self, request, response):
        print("Processing response")
        return response