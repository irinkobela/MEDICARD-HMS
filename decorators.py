# decorators.py
from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    """
    Decorator factory that ensures the current user is logged in via Flask-Login
    and has AT LEAST ONE of the specified roles.

    Example Usage:
    @app.route('/admin-only')
    @login_required
    @roles_required('Admin')
    def admin_view():
        return 'Admin access granted.'

    @app.route('/doctor-or-nurse')
    @login_required
    @roles_required('Doctor', 'Nurse')
    def clinical_view():
        return 'Clinical access granted.'
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check if user is authenticated (should be covered by @login_required too)
            if not current_user.is_authenticated:
                # If somehow @login_required wasn't used, block here
                abort(401) # Unauthorized

            # Check if user object has a 'role' attribute and if it's in the allowed list
            # It's crucial your User model (models/models.py) has the 'role' column/attribute
            if not hasattr(current_user, 'role') or current_user.role not in roles:
                # If user doesn't have the role or role is not allowed, return Forbidden
                print(f"Access Denied: User '{current_user.username}' role '{getattr(current_user, 'role', 'N/A')}' not in required roles {roles}") # Server log
                abort(403) # Forbidden - User is logged in, but doesn't have permission

            # If user is authenticated and has the required role, proceed
            return f(*args, **kwargs)
        return decorated_function
    return wrapper