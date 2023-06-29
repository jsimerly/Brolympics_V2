from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import phonenumbers
import re

User = get_user_model()

password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{8,}$')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password', 'first_name', 'last_name', 'date_of_birth', 'email']

    def validate_phone(self, phone):
        try:
            input_number = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(input_number):
                raise serializers.ValidationError("The phone number entered is not valid")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError("The phone number entered is not valid")

        user_with_phone = User.objects.filter(phone=phone, is_phone_verified=True).first()
        if user_with_phone:
            raise serializers.ValidationError("A user with this phone number already exists and is verified.")
        return phone

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)

        if password is not None:
            user.set_password(password)

        user.save()
        return user
    
    def update(self, user, validated_data):
        for key, value in validated_data.items():
            if key == 'password':
                user.set_password(value)
            else:
                setattr(user, key, value)
        user.save()
        return user
    