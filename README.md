# Pykiq

A [sidekiq](https://sidekiq.org) client library for python 3. It uses a simple redis connection to store jobs in one of sidekiqs redis queues.

## Usage

The same redis connection, i.e. server, port and database, must be used as it is already done for sidekiq. You can store it in a pikiq connector object:

```python

import pykiq
import redis

error_handler = pykiq.error.NullErrorHandler()
conn = redis.Redis(name, port, db)
connector = pykiq.connector.RedisConnector.from_existing_connection(error_handler, conn)

```

This connection can be used to create a pykiq connection: 

```python
kiq = pykiq.Sidekiq(connector)
```

Unfortunately, you cannot use this connection directly, since each job has arguments to process and a queue, in which it is enlisted.

Therefore, an object-oriented approach should be used:

```python
class MyJobs(pykiq.Sidekiq):
    def __init__(self, connector: Connector) -> None:
        super().__init__(connector)
        ...
```

Queues can be declared directly in the constructor. You must re-use the names of the sidekiq queues.

```python
class MyJobs(pykiq.Sidekiq):
    def __init__(self, connector: Connector) -> None:
        super().__init__(connector)
        urgent_queue = pikiq.SidekiqQueue("urgent", self)
```

A job can now easily be added:

```python
class MyJobs(pykiq.Sidekiq):
    def __init__(self, connector: Connector) -> None:
        super().__init__(connector)
        urgent_queue = pikiq.SidekiqQueue("urgent", self)
        self.__clean_up = CleanUpJob(urgent_queue)

    @property
    def clean_up(self):
        return self.__clean_up

class CleanUpJob(pykiq.Job):
    def __init__(self, queue: pikiq.SidekiqQueue) -> None:
        super().__init__(queue, "full::name::of::CleanUpJob")

    def clean_up_at(self, time_span: datetime.timedelta, amount: int):
        return super()._perform_in(time_span, amount)
```

When declaring a new job, the full name of the ruby class including the module namespaces must be added. Each job declares to methods: `_perform_in` and `_perform_async`, where the first takes a timedelta to specify a delay. Please note, that the delay must be positive and should respect network latencies.

Any other argument can be added using the variadic argument list and hence a job should declare its own function with arguments.

The usage now is quite simple:

```python
jobs = MyJobs(connector)
jobs.clean_up.clean_up_at(timedelta(minutes=30), 50)
```

That's it.

## License

This is merely a re-write of sidekiq's ruby code in python. Hence the same license for sidekiq and pykiq are used and the library can be freely distributed according to the LGPLv3.

## Versioning

This library follows semantic versioning 2.0. Any breaking change will produce a new major release. Versions below 1.0 are considered to have a unstable interface.
