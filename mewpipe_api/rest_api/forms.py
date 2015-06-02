from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from rest_api.models import UserAccount

class UserAccountCreationForm(UserCreationForm):
  """
  A form that creates a user, with no privileges, from the given email and
  password.
  """

  def __init__(self, *args, **kargs):
    super(UserAccountCreationForm, self).__init__(*args, **kargs)

  class Meta:
    model = UserAccount

class UserAccountChangeForm(UserChangeForm):
  """A form for updating users. Includes all the fields on
  the user, but replaces the password field with admin's
  password hash display field.
  """

  def __init__(self, *args, **kargs):
    super(UserAccountChangeForm, self).__init__(*args, **kargs)

  class Meta:
    model = UserAccount