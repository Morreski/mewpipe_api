
var NotImplementedError = function() {

  this.name = "NotImplementedError";
  this.message = "Not implemented";

}

NotImplementedError.prototype = Error.prototype;
