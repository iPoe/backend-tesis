from django.middleware.csrf import CsrfViewMiddleware

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        #Return a reason instead of a http response
        return reason
        