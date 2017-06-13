from rest_framework_mongoengine.serializers import DocumentSerializer
from accounts.models import Account
from rest_framework_jwt.settings import api_settings


class AccountSerializer(DocumentSerializer):
    class Meta:
        model = Account
        fields = ('username', 'password')
        write_only_fields = 'password'

    def create(self, validated_data):
        account = Account(username=validated_data['username'])
        account.set_password(validated_data['password'])
        account.save()
        return account

    def update(self, instance, validated_data):
        if validated_data['password'] is not None:
            instance.set_password(validated_data['password'])

        return instance


def create_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    # In MongoDB PK is ObjectId
    user.pk = str(user.pk)

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return 'JWT ' + token
