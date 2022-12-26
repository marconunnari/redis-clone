# Redis Clone

This is a simple implementation of a Redis clone written in Python.
It is not meant to be a fully-featured Redis server, but rather a demonstration of how the Redis protocol works.
I developed it following the challenge on the wonderful website [CodeCrafters](https://codecrafters.io/).

## Features

The following Redis commands are implemented:

- `PING`: Sends a `PONG` response to the client.
- `ECHO`: Echoes back the provided argument to the client.
- `SET`: Sets a key-value pair in the database. Optionally takes a `px` argument to set an expiry time in milliseconds.
- `GET`: Gets the value of a key from the database. If the key has an expiry time set and it has passed, the key-value pair is deleted and `-1` is returned to the client.

## Running the Server

To run the server, simply execute the following command (it requires Python 3):

```
./redis-clone
```

The server will listen on `localhost:6379` for incoming connections.

## Connecting to the Server

You can use any Redis client to connect to the server. For example, to connect to the server using `redis-cli`, run the following command:

```
redis-cli -h localhost -p 6379
```

You should then see a `127.0.0.1:6379>` prompt, where you can enter Redis commands as you would with a regular Redis server.

## Limitations

This Redis clone has several limitations compared to a real Redis server:

- Only a limited set of commands are implemented.
- The database is not persisted to disk, so all data is lost when the server is stopped.
- There is no support for multiple databases or authentication.