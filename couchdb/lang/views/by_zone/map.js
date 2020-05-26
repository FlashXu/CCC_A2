function (doc) {
    if (!doc.type && doc.zone) {
        var date = doc.date.split(' ')[0].split('-')
        var sa = [doc.zone.slice(0, 3), doc.zone.slice(3, 5), doc.zone.slice(5)]
        emit(sa.concat(date), doc.lang);
    }
}