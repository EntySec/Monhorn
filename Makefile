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

archive = ar

ifeq ($(platform), windows)
	compiler = x86_64-w64-mingw32-gcc
else
	compiler = clang
endif

certificate = deps/sign.plist

monhorn_template = monhorn.bin
monhorn_library = libmonhorn.a

src = src
includes = include

cflags = -std=c99

template_sources = src/monhorn/template.c

monhorn_sources = $(src)/base64.c $(src)/channel.c $(src)/console.c $(src)/json.c $(src)/utils.c
monhorn_sources += $(src)/tools.c $(src)/monhorn.c $(src)/evp.c

monhorn_objects = base64.o channel.o console.o json.o utils.o
monhorn_objects += tools.o monhorn.o evp.o

monhorn_cc_flags = $(cflags)
monhorn_cc_flags += -I$(includes)

monhorn_ld_flags = -lssl -lcrypto -L. -lmonhorn

ifeq ($(platform), apple_ios)
	ios_cc_flags = -arch arm64 -arch arm64e -isysroot $(sdk)

	monhorn_cc_flags += $(ios_cc_flags)
else ifeq ($(platform), macos)
	macos_cc_flags = -arch x86_64 -isysroot $(sdk)
	monhorn_cc_flags += $(macos_cc_flags)
endif

.PHONY: all library template clean codesign

all: library template

clean:
	rm -rf $(monhorn_objects) $(monhorn_template) $(monhorn_library)

library:
	$(compiler) $(monhorn_sources) $(monhorn_cc_flags) -c
	$(archive) rcs $(library) $(monhorn_objects)

template: $(monhorn_library)
	$(compiler) $(template_sources) $(monhorn_cc_flags) $(monhorn_ld_flags) -o $(monhorn_template)

codesign: $(monhorn_template)
	ldid -S$(certificate) $(monhorn_template)
