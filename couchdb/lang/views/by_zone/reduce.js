function (keys, values, rereduce) {
    var result = {}
    if (!rereduce) {
        values.forEach(v => result[v] = (result[v] || 0) + 1)
    } else {
        values.forEach(c =>
            Object.keys(c).forEach(lang => result[lang] = (result[lang] || 0) + c[lang])
        )
    }
    return result
}