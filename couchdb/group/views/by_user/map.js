function (doc) {
    var uid = doc._id.split(':')[0]
    emit(uid);
}