from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Use roll_no as the primary identifier since USERNAME_FIELD is 'roll_no'
            if 'roll_no' in kwargs:
                user = User.objects.get(roll_no=kwargs['roll_no'])
            elif username:
                # Check if username is actually a roll_no
                user = User.objects.get(roll_no=username)
            else:
                return None
            
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
