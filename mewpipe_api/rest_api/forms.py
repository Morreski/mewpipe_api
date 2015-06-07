from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserChangeForm
from django import forms

from rest_api.models import UserAccount

class UserAccountCreationForm(forms.ModelForm):

  error_messages = {
    'duplicate_email': _("This email address is already in use."),
    'password_mismatch': _("The two passwords are not the same.")
  }

  password1     = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
  password2     = forms.CharField(label=_("Password Confirmation"), widget=forms.PasswordInput,
    help_text=_("Enter the same password."))

  def __init__(self, *args, **kargs):
    super(UserAccountCreationForm, self).__init__(*args, **kargs)

  class Meta:
    model = UserAccount
    exclude = ['is_staff', 'is_active', 'date_joined', 'watched', 'password']

  def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError(
        self.error_messages['password_mismatch'],
        code='password_mismatch'
      )
    return password2

  def save(self, commit=True):
    instance = super(UserAccountCreationForm, self).save(commit=False)
    instance.set_password(self.cleaned_data.get("password1"))
    if commit:
      instance.save()
    return instance

class UserAccountChangeForm(UserChangeForm):

  def __init__(self, *args, **kargs):
    super(UserAccountChangeForm, self).__init__(*args, **kargs)

  class Meta:
    model = UserAccount
    exclude = ['is_staff', 'is_active', 'date_joined', 'watched', 'password']