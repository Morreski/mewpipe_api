/**
* Dependencies
*/

var express     = require("express");
var app         = express();
var router      = express.Router();
var bodyParser  = require("body-parser");
var morgan      = require("morgan");

global.mongoose = require("mongoose");
global.config   = require("./config");
global.fs       = require("fs");

require("./functions/fs")

/**
* Database
*/

mongoose.connect(config.database.url, function(err){
  if(err) console.error.bind(console, "Connection Error : ");
});

/**
* Middlewares
*/

app.use(bodyParser.json());
app.use(morgan("combined"));

/**
* Router
*/

require("./api/routes")(router);

app.use('/api', router);

/**
* End Config
*/

app.listen(config.port);
console.log("Server is ready !");
