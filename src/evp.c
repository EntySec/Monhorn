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

#include <openssl/evp.h>

void evp_encrypt(FILE *in, FILE *out, char *key, char *iv)
{
    int chunk_size = 512;
    unsigned char inbuf[chunk_size];
    unsigned char outbuf[chunk_size + EVP_MAX_BLOCK_LENGTH];
    int inlen;
    int outlen;

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    EVP_CIPHER_CTX_init(ctx);
    EVP_CipherInit_ex(ctx, EVP_aes_256_cbc(), NULL, NULL, NULL, 1);
//    EVP_CIPHER_CTX_set_key_length(ctx, 16);
    EVP_CipherInit_ex(ctx, NULL, NULL, (const unsigned char*)key, (const unsigned char*)iv, 1);

    while (1) {
        inlen = fread(inbuf, 1, chunk_size, in);
        if (inlen <= 0)
            break;

        if (!EVP_CipherUpdate(ctx, outbuf, &outlen, inbuf, inlen)) {
            EVP_CIPHER_CTX_cleanup(ctx);
            return;
        }
        fwrite(outbuf, 1, outlen, out);
    }

    if (!EVP_CipherFinal_ex(ctx, outbuf, &outlen)) {
        EVP_CIPHER_CTX_cleanup(ctx);
        return;
    }

    fwrite(outbuf, 1, outlen, out);
    EVP_CIPHER_CTX_cleanup(ctx);
    rewind(in);
    rewind(out);
}

void evp_decrypt(FILE *in, FILE *out, char *key, char *iv)
{
    int chunk_size = 512;
    unsigned char inbuf[chunk_size];
    unsigned char outbuf[chunk_size + EVP_MAX_BLOCK_LENGTH];
    int inlen;
    int outlen;

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    EVP_CIPHER_CTX_init(ctx);
    EVP_CipherInit_ex(ctx, EVP_aes_256_cbc(), NULL, NULL, NULL, 0);
//    EVP_CIPHER_CTX_set_key_length(ctx, 16);
    EVP_CipherInit_ex(ctx, NULL, NULL, (const unsigned char*)key, (const unsigned char*)iv, 0);

    while (1) {
        inlen = fread(inbuf, 1, chunk_size, in);
        if (inlen <= 0)
            break;

        if (!EVP_CipherUpdate(ctx, outbuf, &outlen, inbuf, inlen)) {
            EVP_CIPHER_CTX_cleanup(ctx);
            return;
        }
        fwrite(outbuf, 1, outlen, out);
    }

    if (!EVP_CipherFinal_ex(ctx, outbuf, &outlen)) {
        EVP_CIPHER_CTX_cleanup(ctx);
        return;
    }

    fwrite(outbuf, 1, outlen, out);
    EVP_CIPHER_CTX_cleanup(ctx);
    rewind(in);
    rewind(out);
}
