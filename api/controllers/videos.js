var videoModel =  new(require("../models/video"))();
var videoModel =  new(require("../models/video"))();



var viewVideo = function(req, res){
  var id = req.params.id;

  var successCallback = function(video){
    res.status(200);
    res.send(video);
  }

  var errorCallback = function(err){
    console.log(err);
    res.sendStatus(500);
  }

  videoModel.findOneById(id, successCallback, errorCallback);
}

var listVideo = function(req, res){
  var successCallback = function(videos){
    res.status(200);
    res.send(videos);
  }

  var errorCallback = function(err){
    console.log(err);
    res.sendStatus(500);
  }

  videoModel.findAll(successCallback, errorCallback);
}

var addVideo = function(req, res){
  var video = req.body

  var successCallback = function(video){
    res.status(201);
    res.send(video);
  }

  var errorCallback = function(err){
    console.log(err);
    res.sendStatus(500);
  }
  console.log(videoModel);
  videoModel.save(video, successCallback, errorCallback);
}

var editVideo = function(req, res){
  var id = req.params.id;

  var updates = req.params.infos;;

  var successCallback = function(videos){
    res.status(200);
    res.send(video);
  }

  var errorCallback = function(err){
    console.log(err);
    res.sendStatus(500);
  }

  videoModel.edit(id, updates, successCallback, errorCallback);
}

var deleteVideo = function(req, res){
  var id = req.params.id;

  var callback = function(err, element){
    res.status(204);
    res.send(element);
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
