"""
Here we define the API for migrations.

Classically, a migration has two methods which a user may call, up and
down. These will be retained. In addition, there are two optional methods which
will get run on all migrations, check and preflight. These must be overridden in
a subclass to have any effect
"""


class Migration(object):

    name = "base"

    def check(self, connection):
        """Ensures that a given migration ran successfully"""
        return True

    def down(self, connection):
        raise NotImplementedError

    def preflight(self, connection):
        """Operations to run before `self.up` is run"""
        return

    def up(self, connection):
        raise NotImplementedError
