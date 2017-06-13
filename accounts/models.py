from mongoengine import Document, StringField
from django.contrib.auth.hashers import check_password, make_password


class Account(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
