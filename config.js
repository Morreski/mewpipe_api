module.exports = {

    folders : {
        models      : __dirname + "/api/models/",
        controllers : __dirname + "/api/controllers/"
    },
    database : {
        url : "mongodb://localhost/mewpipe"
    },
    access : {
        PUBLIC      : 0,
        PRIVATELINK : 1,
        PRIVATE     : 2
    },
    port : 8080
}
