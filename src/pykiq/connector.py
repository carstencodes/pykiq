#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of pykiq
# (see https://github.com/carstencodes/pykiq).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
""" Definition of a backend connection to communicate with sidekiq. For
    testing purposes, the connection is held abstract.
"""
from abc import abstractmethod
from typing import Optional, Type
from types import TracebackType
from datetime import datetime
from json import dumps as to_json_str

from redis import Redis

from .protocol import SIDEKIQ_QUEUES_NAME, SIDEKIQ_QUEUE_TPL
from .error import ErrorHandler, NullErrorHandler


class Connector:
    """Represents an abstracted connection to the sidekiq backend."""

    def __init__(self, error_handler: ErrorHandler) -> None:
        """Creates a new instance of the connector

        Args:
            error_handler (ErrorHandler): The error handler to use.
        """
        self.__error_handler: ErrorHandler = (
            error_handler or NullErrorHandler()
        )
        self.__connected: bool = False

    @abstractmethod
    def connect(self) -> None:
        """Creates a connection to the backend."""

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnects from the backend."""

    @abstractmethod
    def push_to_queue(
        self, queue_name: str, values: dict, tstamp_key_name: str
    ) -> datetime:
        """Pushes an instance represented by the specified values
            to a queue represented by its name. The timestamp is
            added automatically using the specified key name.

        Args:
            queue_name (str): The name of the queue to use.
            values (dict): The values to pack.
            tstamp_key_name (str): The name of the key to use for the
                    timestamp.

        Returns:
            datetime: The timestamp used for enqueuing.
        """

    def _toggle_connection_state(self) -> None:
        """Switches the connection state from connected to
        disconnected and vice versa."""
        self._connection_state = not self._connection_state

    def __set_connection_state(self, value: bool) -> None:
        """Sets the connection state to the specified value.

        Args:
            value (bool): The new connection state
        """
        self.__connected = value

    def __get_connection_state(self) -> bool:
        """Gets the current connection state.

        Returns:
            bool: The current connection state.
        """
        return self.__connected

    _connection_state = property(
        __get_connection_state, __set_connection_state
    )

    def __enter__(self) -> Optional["Connector"]:
        """Creates a context manager automatically connecting and disconnecting
           this instance.

        Returns:
            Optional[Connector]: The connector.
        """
        try:
            self.connect()
            return self
        except ConnectionError as error:
            self.__error_handler.handle(
                "Error while establishing connection", error
            )
            return None

    def __exit__(
        self, _type: Type, value: Exception, _traceback: TracebackType
    ) -> bool:
        """Leaves the current context by disconnecting this instance.

        Args:
            _type (Type): The error type.
            value (Exception): The exception - if one occurred.
            _traceback (TracebackType): The error stacktrace.

        Returns:
            bool: True, if the exception has been handled.
        """
        if self._connection_state:
            self.disconnect()
        if value is not None:
            self.__error_handler.handle("Connection failure", value)

        return True


class RedisConnector(Connector):
    """A connector instance using a redis in-memory database backend."""

    __REDIS_DEFAULT_PORT: int = 6379
    __REDIS_DEFAULT_DB: int = 0
    __REDIS_DEFAULT_HOST: str = "localhost"

    def __init__(
        self,
        error_handler: ErrorHandler,
        host: str = __REDIS_DEFAULT_HOST,
        port: int = __REDIS_DEFAULT_PORT,
        db: int = __REDIS_DEFAULT_DB,
    ) -> None:
        """Creates a connector instance using a new redis connection.

        Args:
            error_handler (ErrorHandler): The error handler to use.
            host (str, optional): The host to connect to. Defaults to the
                    local host.
            port (int, optional): The port to connect to. Defaults to the
                    redis default port.
            db (int, optional): The database index. Defaults to the first db.
        """
        self.__host: str = host
        self.__port: int = port
        self.__db: int = db
        self.__redis_connection: Optional[Redis] = None
        super().__init__(error_handler)

    @staticmethod
    def from_existing_connection(
        error_handler: ErrorHandler, redis_connection: Redis
    ) -> "RedisConnector":
        """Creates a new redis connector using an existing redis connection.

        Returns:
            RedisConnector: The connector.
        """
        instance: "RedisConnector" = RedisConnector(error_handler)
        instance.reuse_connection(redis_connection)
        return instance

    def connect(self) -> None:
        if self._connection_state:
            raise ConnectionError("Already connected")

        self.__redis_connection = Redis(self.__host, self.__port, self.__db)

        self._toggle_connection_state()

    def reuse_connection(self, redis: Redis) -> None:
        """Discards the current connection information and
           reuses the redis connection.

        Args:
            redis (Redis): The existing redis connection.

        Raises:
            ConnectionError: If this instance is already connected.
        """
        if self._connection_state:
            raise ConnectionError("Already connected")

        self.__redis_connection = redis
        self._toggle_connection_state()

    def disconnect(self) -> None:
        if not self._connection_state:
            raise ConnectionError("Not connected")

        self._toggle_connection_state()
        self.__redis_connection = None

    def push_to_queue(
        self, queue_name: str, values: dict, tstamp_key_name: str
    ) -> datetime:
        if not self._connection_state or self.__redis_connection is None:
            raise ConnectionError("Not connected")

        redis: Redis = self.__redis_connection

        now: datetime = datetime.now()

        data = dict(values)
        data[tstamp_key_name] = now.timestamp()

        encoded_data = to_json_str(data)
        redis.sadd(SIDEKIQ_QUEUES_NAME, queue_name)
        redis.lpush(SIDEKIQ_QUEUE_TPL.format(queue_name), encoded_data)

        return now
