#
# Copyright (c) 2021 Carsten Igel.
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

"""Definition of the basic types.
"""

from abc import ABC, abstractmethod


class NamedObject(ABC):
    """The basic named object class."""

    @abstractmethod
    def get_name(self) -> str:
        """Generates the name of this instance.

        Returns:
            str: The name.
        """

    @abstractmethod
    def get_full_name(self) -> str:
        """Generates the full name of this instance.

        Returns:
            str: The full name of this instance.
        """


class Namespace(ABC):
    """Provides a namespace for Named objects."""

    @abstractmethod
    def get_full_name(self, instance: NamedObject) -> str:
        """Calculates the full name of the named object instance

        Args:
            instance (NamedObject): The named object to wrap up

        Returns:
            str: The full name.
        """
