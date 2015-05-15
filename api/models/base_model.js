
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

  findOneById : function(id, successCallback, errorCallback){
    errorCallback   = errorCallback || function(){};

    var params = {
      _id : id,
    };

    this.find(params, successCallback, errorCallback, false);

  },

  find: function(params, successCallback, errorCallback, many){
    var many = many || true;

    var that = this;

    this.model.find(params, function(err, models){

      if (many) {
        var model = (models.length >= 0) ? models[0] : {};
        err ? errorCallback(err) : successCallback(that._format(model));
        return
      }

      var formatted_models = []
      for (var index in formatted_models) {
        var model = models[index];
        formatted_models.push(that._format(model));
      }

      err ? errorCallback(err) : successCallback(formatted_models);
    });

  },

  findOneOrCreate : function(params, successCallback, errorCallBack) {
    var that = this;
    var success = function(model) {
      if (Object.keys.length(model) > 0) {
        successCallback(model);
      }
      else {
        that.save(params, successCallback, errorCallBack);
      }
    }

    this.model.find(params, success, error, false);
  },

  findAll : function(successCallback, errorCallback, getTheDeleted){
    errorCallback   = errorCallback || function(){};
    getTheDeleted   = getTheDeleted || false;

    var that = this;
    this.model.find({ deleted : getTheDeleted }, function(err, models){
      var model_list = []
      for(var index in models) {
        var model = models[index]
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
        if (model.deleted == undefined) {
          this.model.findByIdAndRemove(id, function(err, nbDeleted){
            callback(err, nbDeleted);
          });
        }
        callback(err, that._format(model));
      });
    }
  }
}

module.exports = BaseModel;
