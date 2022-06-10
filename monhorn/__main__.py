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

from pex.exe import EXE
from pex.string import String


class Monhorn(EXE, String):
    """ Main class of monhorn module.

    This main class of monhorn module is intended for providing
    an implementation of Monhorn manipulation methods.
    """

    templates = f'{os.path.dirname(os.path.dirname(__file__))}/monhorn/templates/'

    def get_template(self, platform: str, arch: str) -> bytes:
        """ Get Monhorn template.

        :param str platform: platform to get Monhorn template for
        :param str arch: architecture to get Monhorn template for
        :return bytes: Monhorn template
        """

        payload = self.templates + platform + '/' + arch + '.bin'

        if os.path.exists(payload):
            return open(payload, 'rb').read()
        return b''

    def encode_data(self, host=None, port=8888):
        if not host:
            data = json.dumps({
                'port': str(port)
            })
        else:
            data = json.dumps({
                'host': host,
                'port': str(port)
            })

        return self.base64_string(data, False)

    def get_monhorn(self, platform: str, arch: str, host: str = '', port: int = 8888) -> bytes:
        """ Get Monhorn.

        :param str platform: platform to get Monhorn for
        :param str arch: arhcitecture to get Monhorn for
        :param str host: host to get Monhorn with
        :param int port: port to get Monhorn with
        :return bytes: Monhorn
        """

        template = self.get_template(platform, arch)

        if not host and not port:
            return template

        return self.executable_replace(
            template, '::data::', self.encode_data(host, port)
        )
