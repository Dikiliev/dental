from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text=(
                                             "Raw passwords are not stored, so there is no way to see this user's password, "
                                             "but you can change the password using <a href=\"../password/\">this form</a>."))

    new_password = forms.CharField(label='New Password', required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm New Password', required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_staff')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
