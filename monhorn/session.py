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

from .console import Console

from hatsploit.lib.loot import Loot
from hatsploit.lib.session import Session

from pex.ssl import OpenSSL
from pex.string import String
from pex.proto.channel import ChannelClient


class MonhornSession(Session, Console, OpenSSL, String, ChannelClient):
    """ Subclass of monhorn module.

    This subclass of monhorn module represents an implementation
    of the Monhorn session for HatSploit Framework.
    """

    loot = Loot()

    monhorn = f'{os.path.dirname(os.path.dirname(__file__))}/monhorn/'
    channel = None

    details = {
        'Post': "",
        'Platform': "",
        'Architecture': "",
        'Type': "monhorn"
    }

    def open(self, client: socket.socket) -> None:
        """ Open the Monhorn session.

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
        """ Close the Monhorn session.

        :return None: None
        """

        self.channel.disconnect()

    def heartbeat(self) -> bool:
        """ Check the Monhorn session heartbeat.

        :return bool: True if the Monhorn session is alive
        """

        return not self.channel.terminated

    def send_command(self, command: str, output: bool = False) -> str:
        """ Send command to the Monhorn session.

        :param str command: command to send
        :param bool output: wait for the output or not
        :return str: command output
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
            self.print_empty
        )

        return ''

    def interact(self) -> None:
        """ Interact with the Monhorn session.

        :return None: None
        """

        self.monhorn_console(self)
