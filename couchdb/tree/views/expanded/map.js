function (doc) {
    if (doc.searched == true)
        emit([doc.expanded, doc.level]);
}