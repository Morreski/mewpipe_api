class InternalError(Exception):
  def __init__(self, code, message, **kwargs):
    self.code     = code
    self.message  = message.format(**kwargs)

  def __str__(self):
    return self.message

class ModelException(InternalError):
  pass
