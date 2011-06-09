"""
Here we define the API for migrations.

Classically, a migration has two methods which a user may call, up and
down. These will be retained.

"""


class Migration(object):

    def up(self, connection):
        raise NotImplementedError

    def down(self, connection):
        raise NotImplementedError
