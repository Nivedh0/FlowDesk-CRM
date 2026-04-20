from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UsernameAwarePasswordResetForm(PasswordResetForm):
    username = forms.CharField(
        max_length=150,
        label=_("Username"),
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = (cleaned_data.get("username") or "").strip()
        email = (cleaned_data.get("email") or "").strip()

        if not username or not email:
            return cleaned_data

        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise forms.ValidationError("No account was found for that username.")

        if not user.email:
            raise forms.ValidationError("This account does not have an email address configured.")

        if user.email.casefold() != email.casefold():
            raise forms.ValidationError("The email address does not match this username.")

        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")

        self.matched_user = user
        cleaned_data["username"] = user.username
        cleaned_data["email"] = user.email
        return cleaned_data

    def get_users(self, email):
        user = getattr(self, "matched_user", None)
        if not user:
            return []

        if user.has_usable_password() and user.email and user.email.casefold() == email.casefold():
            return [user]

        return []
