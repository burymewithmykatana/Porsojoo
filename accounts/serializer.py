from rest_framework import serializers

from accounts.models import User
from accounts.models.otp_token import OtpToken
from accounts.validators import iranian_phone_number_validator


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "email",
        )
        extra_kwargs = {
            "id": {"readonly": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class IranianPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=13, validators=[iranian_phone_number_validator]
    )

    @staticmethod
    def validate_phone_number(value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "User with this phone number does not exist."
            )
        return value


class VerifyOtpTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=13, validators=[iranian_phone_number_validator]
    )
    otp_token = serializers.CharField(max_length=4)

    def validate(self, data):
        phone_number = data["phone_number"]
        otp_token = data["otp_token"]

        if not OtpToken.objects.filter(phone_number=phone_number, code=otp_token).exists():
            raise serializers.ValidationError("Invalid OTP token.")

        return data
