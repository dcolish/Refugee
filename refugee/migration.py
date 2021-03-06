"""
Here we define the API for migrations.

Classically, a migration has two methods which a user may call, up and
down. These will be retained. In addition, there are two optional methods which
will get run on all migrations, check and pre-flight. These must be overridden
in a subclass to have any effect
"""

from collections import namedtuple
import threading


Direction = namedtuple('Direction', 'UP DOWN')._make(range(2))


class MigrationError(Exception):
    """Raised when a Migration Fails"""


class UnknowDirectionError(MigrationError):
    """Raised when an unknown migration direction is given"""


class RegistryLocked(Exception):
    """Raised when the registration is locked and attempted to be modified"""


class Migration(object):
    """
    The API described below is enforced by the Migration Manager.

    Only :py:func:`.down` and :py:func:`.up` are absolutely required.

    The optional :py:func:`.check` and :py:func:`.preflight` are called in order
    to assist with the migration.

    The life-cycle of a migration goes as follows::

        :py:func:`.preflight` -> (:py:func:`.up` | :py:func:`.down`) -> :py:func:`.check`
    """
    name = None

    def check(self, connection):
        """Ensures that a given migration ran successfully"""
        return True

    def down(self, connection):
        """Called when Direction.DOWN == True"""
        raise NotImplementedError

    def preflight(self, connection):
        """Operations to run before `self.up` is run"""
        return True

    def up(self, connection):
        """Called when Direction.UP == True"""
        raise NotImplementedError


migration_tmpl = """\
from refugee import Migration, register


class {cls_name}(Migration):
    name = {migration_name}

    def up(self, connection):
        #TODO implement {name} up migration
        pass

    def down(self, connection):
        #TODO implement {name} down migration
        pass

"""


registry_lock = threading.Lock()


class registry(dict):
    """Lame attempt at a locking registry"""

    def __getitem__(self, key):
        with registry_lock:
            super(dict, self).__getitem__(key)

    def __setitem__(self, key, value):
        with registry_lock:
            super(dict, self).__setitem__(key, value)
