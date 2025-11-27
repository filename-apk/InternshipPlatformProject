# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
#from .admin import setup_admin
from .position import position_views
from .shortlist import shortlist_views
from .StudentView import student_views
from .EmployerView import employer_views
from .StaffView import staff_views


views = [user_views, index_views, auth_views, position_views, shortlist_views, student_views, employer_views, staff_views]
# blueprints must be added to this list