import socket
import threading

from app.resp_decoder import RESPDecoder

database = {}


def handle_ping(client_connection):
    client_connection.send(b"+PONG\r\n")


def handle_echo(client_connection, args):
    client_connection.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))


def handle_set(client_connection, args):
    database[args[0]] = args[1]
    client_connection.send(b"+OK\r\n")


def handle_get(client_connection, args):
    value = database.get(args[0])
    if value is None:
        client_connection.send(b"+(nil)\r\n")
    else:
        client_connection.send(b"$%d\r\n%b\r\n" % (len(value), value))


def handle_connection(client_connection):
    while True:
        try:
            command, *args = RESPDecoder(client_connection).decode()

            if command == b"ping":
                handle_ping(client_connection)
            elif command == b"echo":
                handle_echo(client_connection, args)
            elif command == b"set":
                handle_set(client_connection, args)
            elif command == b"get":
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
