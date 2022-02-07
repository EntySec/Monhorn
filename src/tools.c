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

#include <stdlib.h>
#include <openssl/evp.h>
#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

char *linkStr(char *s1, char *s2, int isPath)
{
    char *separator = "/";

    int length = isPath ? strlen(s1)+strlen(s2)+strlen(separator)+1 : strlen(s1)+strlen(s2)+1;
    int size = isPath ? sizeof(s1)+sizeof(s2)+sizeof(separator)+1 : sizeof(s1)+sizeof(s2)+1;
    char *newStr = (char *) calloc(length, size);
    strcat(newStr, s1);

    if (isPath)
      strcat(newStr, separator);

    strcat(newStr, s2);
    return newStr;
}

char *removeLastChars(char *str, int n)
{
    char *newStr = (char *) malloc(strlen(str));
    strcpy(newStr,str);
    newStr[strlen(newStr)-n] = '\0';
    return newStr;
}

void deleteFile(char *path)
{
    int BUF_SIZE = 4096;
    struct stat path_buff;

    if (stat(path, &path_buff) == -1)
      return;

    off_t fileSize = path_buff.st_size;
    int file = open(path, O_WRONLY);

    if (file == -1)
        return;

    void *buf = malloc(BUF_SIZE);
    memset(buf, 0, BUF_SIZE);

    ssize_t ret = 0;
    off_t shift = 0;
    while ((ret = write(file, buf, ((fileSize - shift >BUF_SIZE) ? BUF_SIZE : (fileSize - shift)))) > 0)
        shift += ret;

    close(file);
    free(buf);
    if (ret == -1)
        return;

    remove(path);
}
