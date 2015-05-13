var Video = mongoose.model("Video", new mongoose.Schema({
  title       : { type : String,  required : true },
  
  author      : { type : mongoose.Schema.ObjectId, ref : "User" },

  description : { type : String },
  views       : { type : Number,  default : 0 },
  access      : { type : Number,  default : 0 },
  shared_nb   : { type : Number,  default : 0 },

  deleted     : { type : Boolean, default : false },
  created     : { type : Date,    default : Date.now },
  modified    : { type : Date,    default : Date.now },
}))

/**
* Export
*/

module.exports = {

  save : function(videoInfos, successCallback, errorCallback){

    successCallback = successCallback || function(){};
    errorCallback   = errorCallback   || function(){};

    var video = new Video(videoInfos);

    video.save(function(err, video){
      err ? errorCallback(err) : successCallback(video);
    });
  },

  findOneById : function(id, successCallback, errorCallback, getTheDeleted){
    errorCallback   = errorCallback || function(){};
    getTheDeleted   = getTheDeleted || false;

    var params = { _id : id };

    params.deleted = getTheDeleted;

    Video.find(params, function(err, video){
      err ? errorCallback(err) : successCallback(video);
    });
  },

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
  }
}

