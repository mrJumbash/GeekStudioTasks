from feed.accounts.models import ConfirmCode, User
from rest_framework import serializers
from zxcvbn import zxcvbn
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=16)
    role = serializers.IntegerField()

    def validate_role(self, role):
        if role not in (1, 2, 3):
            raise ValidationError('Role does not exist!')
        else:
            return role


    def validate_password(self, password):
        result = zxcvbn(password)['score']
        if result < 3:
            raise ValidationError('Use hints for making password!')
        return password

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')


class ConfirmCodeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_user_id(self, user_id):
        try:
            ConfirmCode.objects.get(id=user_id)
        except ConfirmCode.DoesNotExist:
            raise ValidationError(f'User with id ({user_id}) not found')
        return user_id



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

