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
"""The definition of various namespaces
"""


from .connector import QueueNamespace


class EmptyNamespace(QueueNamespace):
    """Represents an empty namespace
    """
    def get_name(self, queue_name: str) -> str:
        return queue_name


class PrefixedNamespace(QueueNamespace):
    """Represents a namespace with a queue.
    """
    def __init__(self, prefix: str) -> None:
        """Creates a new PrefixedNamespace

        Args:
            prefix (str): The namespace prefix.
        """
        super().__init__()
        self.__prefix = prefix

    def get_name(self, queue_name: str) -> str:
        """Gets the name of the prefixed queue.

        Args:
            queue_name (str): The name of the queue

        Returns:
            str: The target queue name.
        """
        prefixed_namespace_template = "{}:{}"
        name: str = super().get_name(queue_name)
        return prefixed_namespace_template.format(self.__prefix, name)
