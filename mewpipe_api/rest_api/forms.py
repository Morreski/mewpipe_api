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

class UpdateProfileForm(forms.ModelForm):

  error_messages = {
      'duplicate_username': _("This username is already in use."),
      'duplicate_email': _("This email adress is already in use."),
      'password_mismatch': _("The two password are not similar."),
      'oldpass_error': _("The old password is not correct."), 
      'new_password_missing': _("If you want to modify your password please fill both of the new password fields.")
  }

  current_password  = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)
  new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput, required=False)
  new_password2 = forms.CharField(label=_("New password confirmartion"), widget=forms.PasswordInput, required=False,
    help_text=_("Enter the same password as above, for verification."))

  class Meta:
    model = UserAccount
    exclude = ['is_staff', 'is_active', 'date_joined', 'watched', 'password']

  def clean_email(self):
    email = self.cleaned_data["email"]

    if email == self.instance.email:
      return email
    try:
      UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
      return email
    raise forms.ValidationError(
      self.error_messages['duplicate_email'],
      code='duplicate_email'
    )

  def clean_username(self):
    username = self.cleaned_data["username"]

    if username == self.instance.username:
      return username
    try:
      UserAccount.objects.get(username=username)
    except UserAccount.DoesNotExist:
      return username
    raise forms.ValidationError(
      self.error_messages['duplicate_username'],
      code='duplicate_email'
    )

  def clean_current_password(self):
    old = self.cleaned_data.get("current_password")

    if not self.instance.check_password(old):
      raise forms.ValidationError(
        self.error_messages['oldpass_error'],
        code='oldpass_error'
      )
    return old

  def clean_new_password2(self):
    password1 = self.cleaned_data.get("new_password1")
    password2 = self.cleaned_data.get("new_password2")
    if (not password1 and password2) or (not password2 and password1):
      raise forms.ValidationError(
        self.error_messages['new_password_missing'],
        code='new_password_missing'
      )
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError(
        self.error_messages['password_mismatch'],
        code='password_mismatch'
      )
    return password2

  def save(self, commit=True):
    instance = super(UpdateProfileForm, self).save(commit=False)
    password1 = self.cleaned_data.get("new_password1")
    if password1:
      instance.set_password(password1)
    if commit:
      instance.save()
    return instance