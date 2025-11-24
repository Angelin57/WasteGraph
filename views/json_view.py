import json

class JSONView:
    @staticmethod
    def success(data=None, message="Success"):
        return {
            'status': 'success',
            'message': message,
            'data': data
        }
    
    @staticmethod
    def error(message="Error", status_code=400):
        return {
            'status': 'error',
            'message': message,
            'status_code': status_code
        }