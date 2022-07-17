"""
MIT License

Copyright (c) 2020-2022 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from hatsploit.core.cli.badges import Badges

from hatsploit.lib.runtime import Runtime
from hatsploit.lib.session import Session
from hatsploit.lib.commands import Commands

from pex.fs import FS


class Console(Badges, Runtime, Commands, FS):
    """ Subclass of monhorn module.

    This subclass of monhorn module is intended for providing
    Monhorn main console.
    """

    prompt = '%linemonhorn%end > '

    core_commands = [
        ('exit', 'Terminate Monhorn session.'),
        ('help', 'Show available commands.'),
        ('quit', 'Stop interaction.')
    ]

    commands = {}

    def check_session(self, session: Session) -> bool:
        """ Check is session alive.

        :param Session session: session to check
        :return bool: True if session is alive
        """

        if session.channel.terminated:
            self.print_warning("Connection terminated.")
            session.close()

            return False
        return True

    def start_monhorn(self, session: Session) -> None:
        """ Start Monhorn.

        :param Session session: session to start Monhorn for
        :return None: None
        """

        commands = session.monhorn + 'commands/' + session.details['Platform'].lower()
        exists, is_dir = self.exists(commands)

        if exists and not is_dir:
            self.commands.update(
                self.load_commands(commands)
            )

        commands = session.monhorn + 'commands/generic'
        exists, is_dir = self.exists(commands)

        if exists and not is_dir:
            self.commands.update(
                self.load_commands(commands)
            )

        for command in self.commands:
            self.commands[command].session = session

    def monhorn_console(self, session: Session) -> None:
        """ Start Monhorn console.

        :param Session session: session to start Monhorn console for
        :return None: None
        """

        self.start_monhorn(session)

        if self.check_session(session):
            while True:
                result = self.catch(self.monhorn_shell, [session])
                if result is not Exception and result:
                    break

    def monhorn_shell(self, session: Session) -> bool:
        """ Start Monhorn shell.

        :param Session session: session to start Monhorn shell for
        :return bool: True if Monhorn shell completed
        """

        command = self.input_empty(self.prompt)

        if command:
            if command[0] == 'quit':
                return True

            elif command[0] == 'help':
                self.print_table("Core Commands", ('Command', 'Description'),
                                 *self.core_commands)

                self.show_commands(self.commands)

            elif command[0] == 'exit':
                session.send_command("exit")
                session.channel.terminated = True
                return True

            else:
                self.check_session(session)
                self.execute_custom_command(command, self.commands)

        return False
