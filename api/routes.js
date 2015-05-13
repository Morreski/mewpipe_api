var controllers  = fs.loadFilesFrom(config.folders.controllers);

module.exports = function(router){

    router.route('/videos')
        .get(controllers.videos.list)
        .post(controllers.videos.add);

    router.route('/videos/:id')
        .get(controllers.videos.view)
        .put(controllers.videos.edit)
        .delete(controllers.videos.delete);
};