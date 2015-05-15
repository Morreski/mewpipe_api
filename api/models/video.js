var Video = mongoose.model("Video", new mongoose.Schema({
  title       : { type : String,  required : true },

    author      : { type : mongoose.Schema.ObjectId, ref : "User" }, //FIXME , required: true },

    description : { type : String },
    views       : { type : Number,  default : 0 },
    access      : { type : Number,  default : 0 },
    shared_nb   : { type : Number,  default : 0 },

    is_online       : { type: Boolean, default: false },
    current_state   : { type: Number, default: 0 },
    confidentiality : { type: Number, default: 0 },

    cover       : {
      data : { type: Buffer, default: null },
      contentType : {type: String, default: null },
      required : false
    },

    deleted     : { type : Boolean, default : false },
    created     : { type : Date,    default : Date.now },
    modified    : { type : Date,    default : Date.now },

    tags : [ {type :mongoose.Schema.ObjectId, ref : "Tag" }]
  }));

var VideoModel = function() {

  this.exposed =  ['title', 'author', 'description', 'views', 'access', 'shared_nb', 'created', 'modified', 'is_online', 'current_state', 'confidentiality' ];
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
