"""
Manages the registration and execution of migrations
"""
from fnmatch import filter as file_filter
from imp import find_module, load_module
from os import makedirs, walk
from os.path import join as pjoin

from sqlalchemy import create_engine

from migration import (
    Direction,
    MigrationError,
    migration_tmpl,
    registry,
    UnknowDirectionError,
    )


def build_engine(connection_string):
    return create_engine(connection_string)

configuration_tmpl = """\
[refugee]
# Adjust this url to your database
bind_url = sqlite:///:memory:
migration_home = {path}
"""

#XXX:dc: think about using entry points for registering migrations as well?
migration_registry = registry()


def register(migration_cls):
    """
    Inserts migration into registry
    """
    global migration_registry
    migration_registry.update({migration_cls.name: migration_cls})
    return migration_cls


class MigrationManager(object):
    engine = None
    configured = False

    def collect(self):
        # Walk self.migration_home and return all potential modules
        for root, dirname, files in walk(self.migration_home):
            for file_name in file_filter(files, "*.py"):
                file_name = file_name.replace('.py', '')
                file = None
                try:
                    if file_name == '__init__':
                        continue
                    file, pathname, description = find_module(
                        file_name, [root])
                    load_module(file_name, file, pathname, description)
                finally:
                    if file is not None:
                        file.close()

    def configure(self, config):
        self.engine = build_engine(config.get('bind_url'))
        self.migration_home = config.get('migration_home')
        self.configured = True

    def new(self, name):
        """
        Build a stub migration with name + auto-id in config['migration_home']

        There is no guarantee this id will be unique for all remote migration
        configurations. Conflicts will require manual management.
        """
        #XXX:dc: assert that the name is somewhat sane and follows python
        # naming conventions
        next_id = 0
        cls_name = '_'.join((name, next_id))
        with open(pjoin(self.migration_home, name), "w+") as new_migration:
            print >> new_migration, migration_tmpl.format(
                cls_name=cls_name, migration_name=name)

    def init(self, directory):
        path = pjoin(directory, 'migrations')
        makedirs(path)
        with open(pjoin(directory, 'refugee.ini'), 'w+') as conf:
            print >> conf, configuration_tmpl.format(path=path)

    def list(self):
        self.collect()
        for k in migration_registry.keys():
            print k

    def run_all(self, direction):
            for key in sorted(migration_registry.keys):
                self.run(key, direction)

    def run(self, key, direction):
        if not self.engine:
            raise AttributeError("No engine configured for MigrationManager")

        connection = self.engine.connect()
        trans = connection.begin()
        try:
            migration = migration_registry[key]()
            if migration.preflight():
                trans = connection.begin()

            if direction == Direction.UP:
                migration.up(connection)
            elif direction == Direction.DOWN:
                migration.down(connection)
            else:
                raise UnknowDirectionError

            if migration.check():
                trans.commit()
            else:
                raise MigrationError("Migration failed consistency checks")
        except Exception, e:
            trans.rollback()
            #XXX:dc: do more to introspect why we failed
            raise e

migration_manager = MigrationManager()
