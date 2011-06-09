"""
Manages the registration and execution of migrations
"""


class Manager(object):

    def register(self, migration):
        """Inserts migration into registry"""
