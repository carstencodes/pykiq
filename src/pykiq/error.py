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
""" Definition of error handling classes.

    The module contains an abstract ErrorHandler class and three simple
    derivations:

    - A NullErrorHandler, which ignores any error.
    - A StdErrErrorHandler writing all errors to stderr
    - A LoggingErrorHandler using the logging module to handle exceptions.
"""

from abc import abstractmethod
import logging
import sys


class ErrorHandler:
    """Basic definition of an error handler."""

    @abstractmethod
    def handle(self, message: str, error: Exception) -> bool:
        """Handles the specified error. A message must be specified describing
           the operation that failed.

        Args:
            message (str): The message describing the current operation.
            error (Exception): The error that encountered.

        Returns:
            bool: A boolean value describing whether the error has been
                  logged or not.
        """


class NullErrorHandler(ErrorHandler):
    """An error handler instance that ignores all errors."""

    def handle(self, message: str, _: Exception) -> bool:
        return True


class StdErrErrorHandler(ErrorHandler):
    """An error handler instance that writes all errors to stderr."""

    def handle(self, message: str, _: Exception) -> bool:
        sys.stderr.write(message)
        return True


class LoggingErrorHandler(ErrorHandler):
    """An error handler instance that writes all errors to a python logging
    module."""

    def __init__(self, logger: logging.Logger = None) -> None:
        """Instantiates a new instance of the logger.

        Args:
            logger (logging.Logger, optional): The logger to take.
                        Will create a new on, if no logger is
                        specified. Defaults to None.
        """
        self.__logger: logging.Logger = logger or logging.getLogger(__file__)

    def handle(self, message: str, error: Exception) -> bool:
        self.__logger.exception(message, exc_info=error)
        return True
