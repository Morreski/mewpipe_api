from django.apps import AppConfig
import watson

class RestAPIAppConfig(AppConfig):
  name = "rest_api"
  verbose_name = "mewpipe restful web service"
  def ready(self):
    for model in ['Video', 'Tag']:
      ClassModel = self.get_model(model)
      watson.register(ClassModel)
