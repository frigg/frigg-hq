from django.db import models


class PRDeploymentManager(models.Manager):

    def create(self, **kwargs):
        """
        Sets the correct port in kwargs before calling super().create(**kwargs).
        The port will not be changed if it is already set.

        Will set the port to the next available port between 49152 and 65535.
        """
        if 'port' not in kwargs:
            last = self.last()
            kwargs['port'] = last.port + 1 if last else 49152
        if kwargs['port'] < 49152 or kwargs['port'] > 65535:
            kwargs['port'] = 49152
        return super().create(**kwargs)
