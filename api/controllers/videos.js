var videoModel =  new(require("../models/video"))();
var tagModel = new(require("../models/tag"))();
var errors = require("../exceptions/base_errors");


var viewVideo = function(req, res){
  var id = req.params.id;

  var successCallback = function(video){
    res.status(200);
    res.send(video);
  }

  var errorCallback = function(err){
    errors.RequestError(res, err);
  }

  videoModel.findOneById(id, successCallback, errorCallback);
}

var listVideo = function(req, res){
  var successCallback = function(videos){
    res.status(200);
    res.send(videos);
  }

  var errorCallback = function(err){
    errors.RequestError(res, err);
  }

  videoModel.findAll(successCallback, errorCallback);
}

var addVideo = function(req, res){
  var video = req.body;
  var tags = video['tags'];

  var errorCallback = function(err){
    errors.RequestError(res, err);
  }

  var successCallback = function(video){

    var bindTagAndVideo = function(tag) {
      tag.videos.push(video._id);
      video.tag.push(tag._id);
      tagModel.save(tag)
      videoModel.save(video);
    }

    for (tagName in tags) {
      tag = tagModel.findOneOrCreate({'name' : tagName}, bindTagAndVideo, errorCallback);
    }

    res.send(video);
  }

  videoModel.save(video, successCallback, errorCallback);
}

var editVideo = function(req, res){
  var id = req.params.id;

  var updates = req.body;

  var successCallback = function(video){
    res.status(200);
    res.send(video);
  }

  var errorCallback = function(err){
    errors.RequestError(res, err);
  }

  videoModel.edit(id, updates, successCallback, errorCallback);
}

var deleteVideo = function(req, res){
  var id = req.params.id;

  var callback = function(err, element){
    res.status(204);
    res.send(element);
  }

  var errorCallback = function(err){
    errors.RequestError(res, err);
  }

  videoModel.delete(id, callback);
}

/**
* Exports
*/

exports.view    = viewVideo;
exports.list    = listVideo;
exports.add     = addVideo;
exports.edit    = editVideo;
exports.delete  = deleteVideo;
