from ConfigParser import SafeConfigParser
from argparse import ArgumentParser
from cmd import Cmd

from refugee.inspector import dump_sql
from refugee.manager import migrations
from refugee.migration import Direction


class RefugeeCmd(Cmd):
    intro = 'Welcome to the Refugee Shell. Type help or ? to list commands\n'
    prompt = 'refugee> '

    def do_dumpsql(self, arg):
        """
        Produces a raw sql dump of the existing database to the best abilities
        of refugee. There will be certain types which are impossible to dump
        currently
        """
        dump_sql(arg)

    def do_down(self, arg):
        """Run down migration with name or numeric id matching arg"""
        print "running down migration"
        migrations.run_one(arg, Direction.DOWN)

    def do_init(self, directory):
        """
        Create a new migrations directory and initialize the configuration
        file in that directory

        :param directory: location to initialize migrations in
        """
        print "initializing migrations in %s" % directory
        migrations.init(directory)

    def do_list(self, arg):
        migrations.list()

    def do_migrate(self, arg):
        """
        Run migrations, If an argument is passed that will be used as the
        stopping point for the migration run
        """
        print "running migrations"
        #XXX:dc: need to interpret the args to allow passing of a specific
        # migration for the stopping point
        migrations.run_all(Direction.UP)

    def do_new(self, name):
        """
        Create a migration with `name`. The migration will also be assigned an
        locally unique id.

        :param name: The named parameter to give the new migration
        """
        print "creating migration %s" % name
        #XXX:dc: assert that name is sane
        migrations.new(name)

    def do_up(self, arg):
        """Run up migration with name or numeric id matching arg"""
        print "running up migration"
        migrations.run(arg, Direction.UP)

    def do_exit(self, arg):
        """Quit the interactive shell"""
        exit()

    def do_quit(self, arg):
        """Quit the interactive shell"""
        exit()

    def default(self, line):
        if line == 'EOF':
            print
            exit()
        else:
            print "Unrecognizable command"
            self.do_help('')

    def emptyline(self):
        # Do nothing with empty lines
        pass


def main():
    cli = RefugeeCmd()
    config = SafeConfigParser()
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help='Configuration File')
    parser.add_argument('command', metavar='CMD', type=str, nargs='?',
                        default='', help="command")
    parser.add_argument('parameters', metavar='ARG', type=str, nargs="*",
                        help="command parameters")

    options = parser.parse_args()

    command = options.command
    parameters = ' '.join(options.parameters)
    if options.config:
        if command == 'init':
            print "Configuration files are not compatible with initialization"
        config.read(options.config)
        migrations.configure(dict(config.items('refugee')))
    if command == '' and parameters == '':
        cli.cmdloop()
    else:
        cli.onecmd(' '.join((command, parameters)))


if __name__ == "__main__":
    main()
