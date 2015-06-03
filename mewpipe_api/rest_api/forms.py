from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from rest_api.models import UserAccount

class UserAccountCreationForm(UserCreationForm):

  def __init__(self, *args, **kargs):
    super(UserAccountCreationForm, self).__init__(*args, **kargs)

  class Meta:
    model = UserAccount

class UserAccountChangeForm(UserChangeForm):

  def __init__(self, *args, **kargs):
    super(UserAccountChangeForm, self).__init__(*args, **kargs)

  class Meta:
    model = UserAccount