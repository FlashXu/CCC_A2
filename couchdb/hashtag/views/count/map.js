function (doc) {
    doc.hashtags.forEach(h => emit(h.toLowerCase()))
}