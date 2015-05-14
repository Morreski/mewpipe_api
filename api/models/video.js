
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
  }));

var VideoModel = function() {

  this.exposed =  ['title', 'author', 'description', 'views', 'access', 'shared_nb', 'created', 'modified'];
  this.model = Video;

}

VideoModel.prototype = require("./base_model");

/**
* Export
*/
module.exports = VideoModel;
