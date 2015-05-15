var format = require("../../functions/format");

var NotImplementedError = function() {

  this.name = "NotImplementedError";
  this.message = "Not implemented";

}

NotImplementedError.prototype = Error.prototype;

var error_base = {
  "ValidationError" : "Missing fields: ${fields}"
};

var RequestError = function(res, err) {
  if (config.DEBUG) {
    console.error(err);
  }

  if (error_base[err.name] != undefined) {
    var field_list = []
    for (field_name in err.errors) {
      field_list.push(field_name);
    }

    var error_data = {
      "fields" : field_list,
      "message" : err.message,
      "full_error" : err,
    }

    var formatted_error = {
      "error" : format(error_base[err.name], error_data)
    }

    res.status(400);
    res.send(formatted_error);
  }
  else {
    var message = (config.DEBUG) ? err : 'INTERNAL SERVER ERROR';
    res.status(500);
    res.send({"error" : message});
  }

};

module.exports = {
  NotImplementedError : NotImplementedError,
  RequestError : RequestError
};
