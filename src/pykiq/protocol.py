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
"""Definition of fields and variables for the Redis storage used by sidekiq.
"""

SIDEKIQ_CLASS_NAME = "class"
SIDEKIQ_SCHEDULE_AT = "at"
SIDEKIQ_QUEUE = "queue"
SIDEKIQ_ARGS = "args"
SIDEKIQ_JOB_ID = "jid"
SIDEKIQ_CREATED = "created_at"
SIDEKIQ_ENQUEUED = "enqueued_at"

SIDEKIQ_QUEUES_NAME = "queues"
SIDEKIQ_QUEUE_TPL = "queue:{}"
