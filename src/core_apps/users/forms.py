from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

#subclass the user change form:
class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User

class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    error_messages = {
        "duplicate_email":"A user with this email already exists"
    }

    #override the default clean email method to check if email already exists:
    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     try:
    #         User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return email
    #     raise forms.ValidationError(self.error_messages["duplicate_email"])

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._meta.get_field("groups")
            User._meta.get_field("user_permissions")
        except (AttributeError, models.FieldDoesNotExist):
            # Exclude groups and user_permissions if they don't exist
            return email
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"])