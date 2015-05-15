
var format_template = function(str, kwargs) {
  for (key in kwargs) {
    var str = str.replace("${" + key + "}", kwargs[key]);
  }

  return str
}

module.exports = format_template;
