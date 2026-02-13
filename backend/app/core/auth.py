from functools import wraps
from flask import request, jsonify

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(current_user, user_role, *args, **kwargs):
            if user_role not in roles:
                return jsonify({'message':'no access for your role'}), 403
            return f(current_user, user_role, *args, **kwargs)
        return decorated
    return wrapper

    
