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
""" Definition of a remote job for sidekiq. This module simply defines an
    abstract definition of a job that must be implemented with a concrete
    method, i.e. the concrete method signature should be used.
"""

from abc import abstractmethod
from typing import Dict, List, Union, Optional
from datetime import timedelta

from .protocol import SIDEKIQ_JOB_ID as JOB_ID_KEY

Primitive = Union[str, int, float, bool]
PrimitiveList = List[Primitive]
PrimitiveMap = Dict[str, Primitive]

JobId = Optional[str]


class Job:
    """Definition of an arbitrary job to execute."""

    def __init__(self, queue: "JobQueue", class_name: str) -> None:
        """Creates a new instance of a job.

        Args:
            queue (JobQueue): The job queue to use.
            class_name (str): The name of the ruby class including the
                  module name.
        """
        self.__klass = class_name
        self.__queue = queue

    @property
    def klass(self) -> str:
        """The name of the entire ruby class that represents the remote job.

        Returns:
            str: The name of the class.
        """
        return self.__klass

    @property
    def retry(self) -> bool:
        """Defines whether the job shall be retried on failure or not.

        Returns:
            bool: The retry flag (True for retry, False for omit and fail)
        """
        return True

    def _perform_async(self, *args) -> JobId:
        """Enqueues this instance for immediate execution.

        Returns:
            JobId: The ID of the remote job.
        """
        return self._perform_in(timedelta(), *args)

    def _perform_in(self, time_span: timedelta, *args) -> JobId:
        """Enqueues this instance for a delayed execution.

        Args:
            time_span (timedelta): The delay to used.

        Returns:
            JobId: The ID of the remote job.
        """
        result: PrimitiveMap = self.__queue.enqueue(self, time_span, *args)
        if JOB_ID_KEY in result.keys():
            value: Primitive = result[JOB_ID_KEY]
            return str(value)

        return None


class JobQueue:
    """Represents a queue for jobs."""

    @abstractmethod
    def enqueue(self, job: Job, delay: timedelta, *args) -> PrimitiveMap:
        """Enqueues the specified job with the given delay and the specified arguments.

        Args:
            job (Job): The job instance to enqueue.
            delay (timedelta): The delay.

        Returns:
            PrimitiveMap: The mangled job
        """
