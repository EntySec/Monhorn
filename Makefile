#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
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

AR = ar
CC = gcc
STRIP = strip

MKDIR = mkdir
MSG = echo
REMOVE = rm

INCLUDE = include
SOURCE = src
BUILD = build

CFLAGS = -std=c99 -Wall -Wextra -pedantic-errors -Werror -I$(INCLUDE) -g
LDFLAGS = -lcrypto

SOURCES := $(wildcard $(SOURCE)/*.c)
OBJECTS := $(patsubst $(SOURCE)/%.c, $(BUILD)/%.o, $(SOURCES))
LIBRARY = libmonhorn.a

SRCS := $(wildcard src/monhorn/*.c)
OBJS := $(patsubst %.c, %.o, $(SRCS))
TARGET = monhorn.bin

Q = @

.PHONY: all build monhorn clean

all: build monhorn

setup:
	$(Q) $(MKDIR) -p $(BUILD)

build: setup $(LIBRARY)

clean:
	$(Q) $(MSG) [Cleaning...]
	$(Q) $(REMOVE) -rf $(OBJECTS) $(BUILD) $(LIBRARY)
	$(Q) $(MSG) [Done]

pwny: $(OBJS)
	$(Q) $(MSG) [Compiling...]
	$(Q) $(CC) $(OBJS) -o $(TARGET) -I$(INCLUDE) $(LDFLAGS) -L. -lmonhorn
	$(Q) $(MSG) [Done]

	$(Q) $(MSG) [Stripping...]
	$(Q) $(STRIP) $(TARGET)
	$(Q) $(MSG) [Done]

%.o: %.c
	$(Q) $(MSG) [Compiling...] $<
	$(Q) $(CC) -c $< -o $@ $(CFLAGS)
	$(Q) $(MSG) [Done]

$(LIBRARY): $(OBJECTS)
	$(Q) $(MSG) [Linking...] $@
	$(Q) $(AR) rcs $@ $(OBJECTS)
	$(Q) $(MSG) [Done]

$(BUILD)/%.o: $(SOURCE)/%.c
	$(Q) $(MSG) [Compiling...] $<
	$(Q) $(CC) $(CFLAGS) -c $< -o $@
