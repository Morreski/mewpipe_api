var fs = require('fs');

fs.loadFilesFrom = function(path){

    var files = {};

    fs.readdirSync(path).forEach(function(file){

        files[fs.removeFileExtension(file)] = require(path + file);

    });

    return files;

}

fs.removeFileExtension = function(filename){
    return filename.replace(/\.[^/.]+$/, "");
}