from argparse import ArgumentParser
from cmd import Cmd

from refugee.inspector import dump_sql


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

    def do_init(self, arg):
        """Run down migration with name or numeric id matching arg"""
        print "initializing migrations"

    def do_migrate(self, arg):
        """Run all up migrations"""
        print "running migrations"

    def do_new(self, arg):
        """Run down migration with name or numeric id matching arg"""
        print "initializing migrations"

    def do_up(self, arg):
        """Run up migration with name or numeric id matching arg"""
        print "running up migration"

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
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help='Configuration File')
    parser.add_argument('command', metavar='CMD', type=str, nargs='?',
                        default='', help="command")
    parser.add_argument('parameters', metavar='ARG', type=str, nargs="*",
                        help="command parameters")

    options = parser.parse_args()
    command = options.command
    parameters = ' '.join(options.parameters)
    if command == '' and parameters == '':
        cli.cmdloop()
    else:
        cli.onecmd(' '.join((command, parameters)))


if __name__ == "__main__":
    main()
