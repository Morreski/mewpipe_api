
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

    var params = { _id : id };

    params.deleted = getTheDeleted;

    var that = this;
    this.model.find(params, function(err, video){
      err ? errorCallback(err) : successCallback(that._format(video));
    });
  },
/*
  findAll : function(successCallback, errorCallback, getTheDeleted){
    errorCallback   = errorCallback || function(){};
    getTheDeleted   = getTheDeleted || false;

    Video.find({ deleted : getTheDeleted }, function(err, videos){
        err ? errorCallback(err) : successCallback(videos);
    });
  },

  edit : function(id, updates, successCallback, errorCallback){
    errorCallback   = errorCallback || function(){};

    updates.modified = Date.now();

    Video.findByIdAndUpdate(id, updates, function(err, video){
        err ? errorCallback(err) : successCallback(video);
    });
  },

  delete : function(id, callback, forcedDeletion){
    callback        = callback || function(){};
    forcedDeletion  = forcedDeletion || false;

    if(forcedDeletion){
      Video.findByIdAndRemove(id, function(err, nbDeleted){
        callback(err, nbDeleted);
      });
    }else{
      var updates = {
        deleted   : true,
        modified  : Date.now()
      };

      Video.findByIdAndUpdate(id, updates, function(err, video){
        callback(err, video);
      });
    }
  }*/
}

module.exports = BaseModel;
