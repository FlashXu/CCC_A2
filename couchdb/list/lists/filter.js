function(head, req) {
    send('{"rows" : [\n')
    var sep = ''
    while (row = getRow()) {
        if (row.value > (req.query.threshold || 0)) {
            send(sep + JSON.stringify(row))
            sep = ','
        }
    }
    send('\n]}')
}