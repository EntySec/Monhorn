"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    details = {
        'Category': "crypto",
        'Name': "decrypt",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Decrypt path with AES 256 cipher.",
        'Usage': "decrypt <path> <key> <iv>",
        'MinArgs': 3
    }

    def run(self, argc, argv):
        data = str({
            'path': argv[1],
            'key': argv[2],
            'iv': argv[3]
        })

        self.session.send_command(f"{argv[0]} '{data}'")
