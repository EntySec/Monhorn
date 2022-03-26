#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
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

from hatvenom import HatVenom

from pex.tools.type import TypeTools
from pex.tools.string import StringTools


class Monhorn(StringTools):
    hatvenom = HatVenom()
    type_tools = TypeTools()

    templates = f'{os.path.dirname(os.path.dirname(__file__))}/monhorn/templates/'

    def get_template(self, platform, arch):
        payload = self.templates + platform + '/' + arch + '.bin'

        if os.path.exists(payload):
            return open(payload, 'rb').read()
        return None

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

        return self.base64_string(data)

    def get_monhorn(self, platform, arch, host=None, port=8888):
        template = self.get_template(platform, arch)

        if not host and not port:
            return template

        for executable in self.type_tools.formats:
            if platform in self.type_tools.formats[executable]:
                return self.hatvenom.generate(executable, arch, template, {
                    'data': self.encode_data(host, port)
                })

        return template
