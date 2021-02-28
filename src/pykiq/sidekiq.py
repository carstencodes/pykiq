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
""" Contains the Sidekiq main worker class that can be used to manage
    the remote jobs.
"""
from datetime import timedelta, datetime
from typing import Tuple, Optional, Union
from secrets import token_hex

from .base import NamedObject, Namespace
from .connector import Connector
from .job import Job, JobQueue, PrimitiveMap
from .protocol import (
    SIDEKIQ_JOB_ID,
    SIDEKIQ_ENQUEUED,
    SIDEKIQ_CLASS_NAME,
    SIDEKIQ_SCHEDULE_AT,
    SIDEKIQ_ARGS,
    SIDEKIQ_CREATED,
    SIDEKIQ_QUEUE,
    SIDEKIQ_QUEUE_TPL,
)


class Sidekiq:
    """Represents a sidekiq connection. Instance of this class
    can be used to push new jobs to new or existing job
    queues using a redis connection.
    """

    def __init__(
        self, connector: Connector, queue_namespace: Optional[NamedObject]
    ) -> None:
        """Creates a new instance.

        Args:
            connector (Connector): The remote connection to use.
            queue_namespace (Optional[QueueNamespace]): The queue namespace to use
        """
        self.__connector: Connector = connector
        self.__queue_namespace = queue_namespace

    def push_to_queue(
        self, queue_name: Union[str, NamedObject], mapped_args: PrimitiveMap
    ) -> Tuple[str, PrimitiveMap]:
        """Pushes the mapped execution arguments to the queue using the
           current connection.

        Args:
            queue_name (str): The name of the queue
            mapped_args (PrimitiveMap): The mapped execution arguments
            for the sidekiq job.

        Returns:
            Tuple[str, PrimitiveMap]: A tuple containing the job id and the
                  resulting parameters.
        """
        jid = Sidekiq.__generate_jid()
        result: dict = dict(mapped_args)
        result[SIDEKIQ_JOB_ID] = jid

        timestamp: datetime = self.__connector.push_to_queue(
            queue_name, result, SIDEKIQ_ENQUEUED, self.__queue_namespace
        )
        result[SIDEKIQ_ENQUEUED] = timestamp.timestamp()

        return (jid, result)

    @staticmethod
    def __generate_jid() -> str:
        """Generates a job id for sidekiq. This must by a valid 12 byte hex value.

        Returns:
            str: The Job ID
        """
        number_of_bytes_in_jid: int = 12

        return token_hex(number_of_bytes_in_jid)


class _EmptySidekiqNamespace(Namespace):
    """Implementation of a namespace for the sidekiq redis queues.
    """
    def get_full_name(self, instance: NamedObject) -> str:
        """Creates a default full name for the queue.

        Args:
            instance (NamedObject): The named object to wrap up.

        Returns:
            str: The sidekiq target queue name.
        """
        return SIDEKIQ_QUEUE_TPL.format(instance.get_name())


class SidekiqQueue(JobQueue, NamedObject):
    """A simple job queue using a sidekiq backend."""

    def __init__(
        self, name: str, kiq: Sidekiq, namespace: Optional[Namespace] = None
    ) -> None:
        """Initializes a new instance.

        Args:
            name (str): The name of the queue to use. Must exist in sidekiq.
            kiq (Sidekiq): The sidekiq connection.
        """
        super().__init__()
        self.__queue_name = name
        self.__sidekiq = kiq
        self.__namespace = namespace or _EmptySidekiqNamespace()

    def enqueue(self, job: Job, delay: timedelta, *args) -> PrimitiveMap:
        """Enqueues the specified job with the given delay and the
           specified arguments to a sidekiq redis queue.

        Args:
            job (pykiq.job.Job): The job instance to enqueue.
            delay (timedelta): The delay.

        Returns:
            PrimitiveMap: The mangled job
        """
        now: datetime = datetime.now()
        schedule_at: datetime = now + delay
        data = dict()
        data[SIDEKIQ_CLASS_NAME] = job.klass
        data[SIDEKIQ_SCHEDULE_AT] = schedule_at.timestamp()
        data[SIDEKIQ_ARGS] = list(args)
        data[SIDEKIQ_CREATED] = now.timestamp()
        data[SIDEKIQ_QUEUE] = self.__queue_name

        (jid, result) = self.__sidekiq.push_to_queue(self, data)
        result[SIDEKIQ_JOB_ID] = jid

        return result

    def get_name(self) -> str:
        return self.__queue_name

    def get_full_name(self) -> str:
        return self.__namespace.get_full_name(self)
