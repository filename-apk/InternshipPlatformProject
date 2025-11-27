from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, current_user

def login_required(*required_classes):
    """
    Decorator that requires JWT authentication and checks if the user is an instance
    of one or more specified classes (e.g., Employer, Student, Staff).
    
    Usage:
        @login_required(Employer)
        def employer_only_endpoint():
            ...
        
        @login_required(Employer, Staff)
        def employer_or_staff_endpoint():
            ...
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user = current_user
            
            # Check if user is an instance of ANY of the required classes
            for required_class in required_classes:
                # Primary check: isinstance
                if isinstance(user, required_class):
                    return f(*args, **kwargs)
                
                # Fallback: check polymorphic identity string
                # (In case SQLAlchemy didn't load the proper subclass)
                if hasattr(user, 'type') and hasattr(required_class, '__mapper_args__'):
                    polymorphic_identity = required_class.__mapper_args__.get('polymorphic_identity')
                    if user.type == polymorphic_identity:
                        return f(*args, **kwargs)
            
            # If no match found, deny access
            class_names = ', '.join([cls.__name__ for cls in required_classes])
            return jsonify({
                'error': 'Unauthorized',
                'message': f'Access requires one of: {class_names}'
            }), 403

        return decorated_function
    return decorator
