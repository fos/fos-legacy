def ws_send(socko, message):
    socko.send('\x00' + str(message).encode('utf-8') + '\xff')