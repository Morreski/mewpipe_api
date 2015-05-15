
var Video = mongoose.model("Video", new mongoose.Schema({
    title       : { type : String,  required : true },

    author      : { type : mongoose.Schema.ObjectId, ref : "User", required: true },

    description : { type : String },
    views       : { type : Number,  default : 0 },
    access      : { type : Number,  default : 0 },
    shared_nb   : { type : Number,  default : 0 },

    is_online       : { type: Boolean, default: false },
    current_state   : { type: Number, default: 0 },
    confidentiality : { type: Number, default: 0 },

    cover       : {
      data : { type: Buffer, required: true },
      contentType : {type: String, required : true }
    },

    deleted     : { type : Boolean, default : false },
    created     : { type : Date,    default : Date.now },
    modified    : { type : Date,    default : Date.now },
  }));

var VideoModel = function() {

  this.exposed =  ['title', 'author', 'description', 'views', 'access', 'shared_nb', 'created', 'modified'];
  this.model = Video;


  this.STATE_CHOICE = {
    "NEW" : 0,
    "UPLOADED" : 1,
    "AVAILABLE" : 2
  }

  this.CONFIDENTIALITY_CHOICE = {
    "PUBLIC" : 0,
    "PRIVATE_LINK" : 1,
    "AUTH_USER" : 2
  }

}

VideoModel.prototype = require("./base_model");

/**
* Export
*/
module.exports = VideoModel;
