
var BaseModel = {

  _default_exposed : ['id'],
  exposed : [],
  model : undefined,
  _format : function(model) {
    var exposed = this.exposed.concat(this._default_exposed);
    var formatted_model = {};

    for (var key in model) {
      if (~exposed.indexOf(key)) {
        formatted_model[key] = model[key];
      }
    }
    return formatted_model;
  },

  save : function(modelAttributes, successCallback, errorCallback){

    successCallback = successCallback || function(){};
    errorCallback   = errorCallback   || function(){};

    var modelInstance = new this.model(modelAttributes);

    var that = this;
    modelInstance.save(function(err, model) {
      err ? errorCallback(err) : successCallback(that._format(modelInstance));
    });
  },

  findOneById : function(id, successCallback, errorCallback, getTheDeleted){
    errorCallback   = errorCallback || function(){};
    getTheDeleted   = getTheDeleted || false;

    var params = {
      _id : id,
      deleted : getTheDeleted
    };

    var that = this;
    this.model.findOne(params, function(err, model){
      err ? errorCallback(err) : successCallback(that._format(model));
    });
  },

  findAll : function(successCallback, errorCallback, getTheDeleted){
    errorCallback   = errorCallback || function(){};
    getTheDeleted   = getTheDeleted || false;

    var that = this;
    this.model.find({ deleted : getTheDeleted }, function(err, models){
      var model_list = []
      for(index in models) {
        model = models[index]
        model_list.push(that._format(model));
      }
        err ? errorCallback(err) : successCallback(model_list);
    });
  },

  edit : function(id, updates, successCallback, errorCallback){
    errorCallback   = errorCallback || function(){};

    var that = this;
    this.model.findByIdAndUpdate(id, updates, {'new': true}, function(err, model){
        err ? errorCallback(err) : successCallback(that._format(model));
    });
  },

  delete : function(id, callback, forcedDeletion){
    callback        = callback || function(){};
    forcedDeletion  = forcedDeletion || false;

    if(forcedDeletion){
      this.model.findByIdAndRemove(id, function(err, nbDeleted){
        callback(err, nbDeleted);
      });
    }else{
      var updates = {
        deleted   : true,
        modified  : Date.now()
      };

      var that = this;
      this.model.findByIdAndUpdate(id, updates, function(err, model){
        callback(err, that._format(model));
      });
    }
  }
}

module.exports = BaseModel;
