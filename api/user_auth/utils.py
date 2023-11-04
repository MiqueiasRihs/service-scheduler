from rest_framework_simplejwt.tokens import RefreshToken

from api.user_auth.serializers import UserSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_user_professional_data(user):
    user_data = UserSerializer(user).data
    tokens = get_tokens_for_user(user)
    return {**user_data, **tokens}