#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (C) 2014, 2018, 2019 Brandon M. Pace
#
# This file is part of Quick IP Converter
#
# Quick IP Converter is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Quick IP Converter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Quick IP Converter.
# If not, see <https://www.gnu.org/licenses/>.


import enum


# list of bit-masks for each octet of an IPv4 address
V4MASKS = [255 << (8*octet_offset) for octet_offset in range(4)]


V4MAXVAL = int('0xffffffff', 16)  # 4294967295 or 255.255.255.255


# enum values that can be used for index of the IP_RE*LIST items
@enum.unique
class ADDRTYPE(enum.IntEnum):
    NONE = -1
    DEC = 0
    HEX = 1
    DOTTED = 2
