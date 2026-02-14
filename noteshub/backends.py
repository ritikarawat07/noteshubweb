from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Use roll_no as the primary identifier since USERNAME_FIELD is 'roll_no'
            if 'roll_no' in kwargs:
                roll_no = kwargs['roll_no']
            elif username:
                roll_no = username
            else:
                print("DEBUG BACKEND: No roll_no or username provided")
                return None
            
            print(f"DEBUG BACKEND: Looking for user with roll_no: {roll_no}")
            try:
                user = User.objects.get(roll_no=roll_no)
                print(f"DEBUG BACKEND: Found user: {user}")
            except User.DoesNotExist:
                print(f"DEBUG BACKEND: User with roll_no '{roll_no}' does not exist")
                return None
            print(f"DEBUG BACKEND: Found user {user}, is_teacher={user.is_teacher}, dob={user.dob}")
            
            # Additional DOB validation for teachers if provided
            if 'dob' in kwargs and user.is_teacher:
                print(f"DEBUG BACKEND: User DOB type: {type(user.dob)}, value: {user.dob}")
                print(f"DEBUG BACKEND: Provided DOB type: {type(kwargs['dob'])}, value: {kwargs['dob']}")
                print(f"DEBUG BACKEND: User DOB string: {str(user.dob)}")
                print(f"DEBUG BACKEND: Provided DOB string: {str(kwargs['dob'])}")
                print(f"DEBUG BACKEND: Date comparison: {user.dob} == {kwargs['dob']} = {user.dob == kwargs['dob']}")
                print(f"DEBUG BACKEND: String comparison: '{str(user.dob)}' == '{str(kwargs['dob'])}' = {str(user.dob) == str(kwargs['dob'])}")
                
                # Try both direct comparison and string comparison
                if user.dob != kwargs['dob'] and str(user.dob) != str(kwargs['dob']):
                    print(f"DEBUG BACKEND: DOB mismatch - both comparisons failed!")
                    return None
                print(f"DEBUG BACKEND: DOB matches!")
            
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
