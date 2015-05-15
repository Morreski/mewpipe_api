var User = mongoose.model("User", new mongoose.Schema({
  firstName       : { type : String,  required : true },
  lastName        : { type : String,  required : true },
  username        : { type : String,  required : true },

  openID          : { type : String },
  nbVideosViewed  : { type : Number,  default : 0 },

  avatar          : {
    data : { type: Buffer, required : true },
    contentType : { type: String, required : true }
  },

  deleted         : { type : Boolean, default : false },
  created         : { type : Date,    default : Date.now },
  modified        : { type : Date,    default : Date.now },
}))

var UserModel = function() {

  this.model = User;
  this.exposed = [] //TODO

}
