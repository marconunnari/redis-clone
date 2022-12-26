import socket
import threading
import time

from .resp_decoder import RESPDecoder

database = {}


def handle_ping(client_connection):
    client_connection.send(b"+PONG\r\n")


def handle_echo(client_connection, args):
    client_connection.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))


def handle_set(client_connection, args):
    expiry = None
    # Check for "px" argument and extract expiry value
    if b"px" in args:
        expiry_index = args.index(b"px") + 1
        expiry = int(args[expiry_index])
        expiry = int(time.time() * 1000) + expiry
        args = args[: expiry_index - 1] + args[expiry_index + 1 :]

    database[args[0]] = (args[1], expiry)
    client_connection.send(b"+OK\r\n")


def handle_get(client_connection, args):
    key = args[0]
    entry = database.get(key)

    if entry is None:
        client_connection.send(b"$-1\r\n")
        return

    value, expiry = entry
    if expiry is not None and expiry <= int(time.time() * 1000):
        del database[key]
        client_connection.send(b"$-1\r\n")
    else:
        client_connection.send(b"$%d\r\n%b\r\n" % (len(value), value))


def handle_connection(client_connection):
    while True:
        try:
            command, *args = RESPDecoder(client_connection).decode()
            command = command.decode("ascii").lower()
            if command == "ping":
                handle_ping(client_connection)
            elif command == "echo":
                handle_echo(client_connection, args)
            elif command == "set":
                handle_set(client_connection, args)
            elif command == "get":
                handle_get(client_connection, args)
            else:
                client_connection.send(b"-ERR unknown command\r\n")
        except ConnectionError:
            break  # Stop serving if the client connection is closed


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        client_connection, _ = server_socket.accept()  # wait for client
        threading.Thread(target=handle_connection, args=(client_connection,)).start()


if __name__ == "__main__":
    main()
