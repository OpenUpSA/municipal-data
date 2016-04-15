from utils import jsonify


class ApiErrorHandler(object):
    """ Return API 500-level errors as JSON. """
    def process_exception(self, request, exception):
        if request.path.startswith('/api/'):
            return jsonify({
                'status': 'error',
                'message': exception.message,
            }, status=500)
