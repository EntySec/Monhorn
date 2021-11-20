#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import json

from hatsploit.lib.session import Session
from hatsploit.lib.commands import Commands

from hatsploit.utils.telnet import TelnetClient


class MonhornSession(Session, TelnetClient):
    commands = Commands()

    prompt = '%linemonhorn%end > '
    monhorn = f'{os.path.dirname(os.path.dirname(__file__))}/monhorn/commands/'

    client = None

    details = {
        'Platform': "",
        'Type': "monhorn"
    }

    def open(self, client):
        self.client = self.open_telnet(client)

    def close(self):
        self.client.disconnect()

    def heartbeat(self):
        return not self.client.terminated

    def send_command(self, command, output=False, timeout=10):
        commands = self.format_commands(command)

        if len(commands) > 1:
            args = ' '.join(commands[1:])
        else:
            args = None

        command_data = json.dumps({
            'cmd': commands[0],
            'args': args
        })

        output = self.client.send_command(command_data, output, timeout)
        return output

    def interact(self):
        self.print_empty()

        if self.client.terminated:
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
                    self.commands.show_commands(monhorn)
                    continue

                self.commands.execute_custom_command(commands, monhorn)

                if commands[0] == 'exit':
                    self.client.terminated = True
                    self.print_warning("Connection terminated.")
                    return
