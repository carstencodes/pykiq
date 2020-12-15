#!/usr/bin/env python3
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

import sys
import os
from datetime import timedelta, datetime

sys.path.append(os.path.join(sys.path[0], "..", "src"))

from pykiq import Sidekiq, SidekiqQueue, Job, JobId, Connector  # noqa: E402


class ConsoleConnector(Connector):
    def connect(self) -> None:
        self._toggle_connection_state()
        return super().connect()

    def disconnect(self) -> None:
        self._toggle_connection_state()
        return super().disconnect()

    def push_to_queue(
        self, queue_name: str, values: dict, tstamp_key_name: str
    ) -> datetime:
        return datetime.now()


class SayHelloJob(Job):
    def __init__(self, queue: SidekiqQueue) -> None:
        super().__init__(queue, "SayHello")

    def perform_in(self, time_span: timedelta, what: str) -> JobId:
        return super()._perform_in(time_span, what)

    def perform_async(self, what: str) -> JobId:
        return super()._perform_async(what)


class MyJobQueue(Sidekiq):
    def __init__(self, connector: Connector) -> None:
        super().__init__(connector)
        important: SidekiqQueue = SidekiqQueue("important", self)
        regular: SidekiqQueue = SidekiqQueue("regular", self)

        assert important != regular

        low: SidekiqQueue = SidekiqQueue("low", self)

        self.__say: SayHelloJob = SayHelloJob(low)

    @property
    def say(self) -> SayHelloJob:
        return self.__say


if __name__ == "__main__":
    queue: MyJobQueue = MyJobQueue(ConsoleConnector(None))
    in_one_minute: timedelta = timedelta(minutes=1.0)
    id = queue.say.perform_in(in_one_minute, "Hello")
    print(id)
