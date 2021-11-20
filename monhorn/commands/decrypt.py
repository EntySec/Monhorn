#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import json

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    details = {
        'Category': "ransomware",
        'Name': "decrypt",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Decrypt every data from the path.",
        'Usage': "decrypt <path> <key> <iv>",
        'MinArgs': 3
    }

    def run(self, argc, argv):
        data = json.dumps({
            'path': argv[1],
            'key': argv[2],
            'iv': argv[3]
        })

        self.session.send_command(f"{argv[0]} '{data}'")
