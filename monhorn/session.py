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

import os
import json
import socket

from hatsploit.lib.loot import Loot
from hatsploit.lib.session import Session
from hatsploit.lib.commands import Commands

from pex.ssl import OpenSSL
from pex.string import String
from pex.proto.channel import ChannelClient


class MonhornSession(Session, OpenSSL, String, ChannelClient):
    """ Subclass of monhorn module.

    This subclass of monhonr module represents an implementation
    of Monhorn session for HatSploit Framework.
    """

    loot = Loot()
    commands = Commands()

    prompt = '%linemonhorn%end > '
    monhorn = f'{os.path.dirname(os.path.dirname(__file__))}/monhorn/commands/'

    channel = None

    details = {
        'Post': "",
        'Platform': "",
        'Architecture': "",
        'Type': "monhorn"
    }

    def open(self, client: socket.socket) -> None:
        """ Open Monhorn session.

        :param socket.socket client: client to open session with
        :return None: None
        """

        client = self.wrap_client(
            client,
            self.loot.random_loot('key'),
            self.loot.random_loot('crt')
        )

        self.channel = self.open_channel(client)

    def close(self) -> None:
        """ Close Monhorn session.

        :return None: None
        """

        self.channel.disconnect()

    def heartbeat(self) -> bool:
        """ Check Monhorn session heartbeat.

        :return bool: True of Monhorn session is alive
        """

        return not self.channel.terminated

    def send_command(self, command: str, output: bool = False, decode: bool = True) -> str:
        """ Send command to Monhorn session.

        :param str command: command to send
        :param bool output: wait for the output or not
        :param :
        """

        args = ''
        token = self.random_string(8)
        commands = self.format_commands(command)

        if len(commands) > 1:
            args = ' '.join(commands[1:])

        command_data = json.dumps({
            'cmd': commands[0],
            'args': args,
            'token': token
        })

        self.channel.send_token_command(
            command_data,
            token,
            output,
            decode,
            self.print_empty
        )

        return ''

    def interact(self):
        self.print_empty()

        if self.channel.terminated:
            self.print_warning("Connection terminated.")
            return

        self.print_process("Loading Monhorn commands...")
        commands = self.monhorn

        monhorn = self.commands.load_commands(commands)
        for command in monhorn:
            monhorn[command].session = self

        self.print_information(f"Loaded {len(monhorn)} commands.")
        self.print_empty()

        while True:
            commands = self.input_empty(self.prompt)

            if commands:
                if commands[0] == 'quit':
                    break

                elif commands[0] == 'help':
                    self.print_table("Core Commands", ('Command', 'Description'), *[
                        ('exit', 'Terminate Monhorn session.'),
                        ('help', 'Show available commands.'),
                        ('quit', 'Stop interaction.')
                    ])

                    self.commands.show_commands(monhorn)
                    continue

                if commands[0] == 'exit':
                    self.send_command("exit")
                    self.channel.terminated = True

            if self.channel.terminated:
                self.print_warning("Connection terminated.")
                self.close()
                break

            if commands:
                self.commands.execute_custom_command(commands, monhorn)
