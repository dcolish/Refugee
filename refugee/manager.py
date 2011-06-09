"""
Manages the registration and execution of migrations
"""
from sqlalchemy import create_engine


def build_engine(connection_string):
    return create_engine(connection_string)


class MigrationManager(object):
    _registry = {}
    engine = None

    def configure(self, config):
        self.engine = build_engine(config.get('refugee.bind_url'))

    def register(self, migration_cls):
        """Inserts migration into registry"""
        self._registry.update(migration_cls.name, migration_cls)

    def run(self, direction):
            for key in sorted(self._registry.keys):
                self.run_one(key, direction)

    def run_one(self, key, direction):
        if not self.engine:
            raise AttributeError("No engine configured for MigrationManager")

        connection = self.engine.connect()
        trans = connection.begin()
        try:
            migration = self._registry[key]
            migration.preflight()
            getattr(migration, direction)(connection)
            migration.check()
            trans.commit()
        except Exception, e:
            trans.rollback()
            #XXX:dc: do more to introspect why we failed
            raise e

migrations = MigrationManager()
