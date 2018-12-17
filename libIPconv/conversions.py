#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (C) 2014, 2018 Brandon M. Pace
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


from .convregex import *
from .globals import *


def convertStrToType(input_val: str, input_type: int, output_type: int, reverse: bool = False, safe: bool = False) -> str:
    """
    Be sure to use isValidIPv4() before this to sanity-check your input!
    :param input_val: str value to convert
    :param input_type: int value type from ADDRTYPE enum determining what the source type is
    :param output_type: int value type from the ADDRTYPE enum determining what the destination type is
    :param reverse: bool for whether or not to reverse the byte-order
    :return: str converted value or '' on error/failure
    """
    return_value = ''
    try:
        if input_type == output_type:
            raise ValueError('output_type should be different than input_type')

        if input_type == ADDRTYPE.DEC:
            if output_type == ADDRTYPE.DOTTED:
                return_value = decStrToDottedQuadStr(input_val, reverse)
            elif output_type == ADDRTYPE.HEX:
                return_value = decStrToHexStr(input_val, reverse)
        elif input_type == ADDRTYPE.DOTTED:
            if output_type == ADDRTYPE.DEC:
                return_value = dottedQuadStrToDecStr(input_val, reverse)
            elif output_type == ADDRTYPE.HEX:
                return_value = dottedQuadStrToHexStr(input_val, reverse)
        elif input_type == ADDRTYPE.HEX:
            if output_type == ADDRTYPE.DEC:
                return_value = hexStrToDecStr(input_val, reverse)
            elif output_type == ADDRTYPE.DOTTED:
                int_value = hexStrToDecStr(input_val, False)
                return_value = decStrToDottedQuadStr(int_value, reverse)
    except ValueError:
        if not safe:
            raise
        else:
            return ''
    else:
        return return_value


def decStrToDottedQuadStr(input_value: str, reverse: bool = False) -> str:
    if RECLIST[ADDRTYPE.DEC].fullmatch(input_value):
        return decToDottedQuadStr(int(input_value), reverse)
    else:
        return ''


def decToDottedQuadList(input_value: int, reverse: bool = False) -> list:
    if (input_value < 0) or (input_value > V4MAXVAL):
        raise ValueError(f'Input value is outside of IPv4 range: {input_value}')
    if reverse:
        byte_order = 'little'
    else:
        byte_order = 'big'
    return [octet for octet in input_value.to_bytes(4, byte_order)]


def decStrToHexStr(input_value: str, reverse: bool = False) -> str:
    return_value = ''
    if input_value:
        if reverse:
            byte_order = 'little'
        else:
            byte_order = 'big'
        int_value = int(input_value)
        return_value = int_value.to_bytes(((int_value.bit_length() + 7) // 8), byte_order).hex()
    return return_value


def decToDottedQuadStr(input_value: int, reverse: bool = False) -> str:
    return '.'.join([str(octet) for octet in decToDottedQuadList(input_value, reverse)])


def dottedQuadStrToDecStr(input_value: str, reverse: bool = False) -> str:
    split_value = [int(value) for value in input_value.split('.')]
    if reverse:
        byte_order = 'little'
    else:
        byte_order = 'big'
    return str(int.from_bytes(split_value, byte_order))


def dottedQuadStrToHexStr(input_value: str, reverse: bool = False) -> str:
    split_value = [int(value) for value in input_value.split('.')]
    if reverse:
        split_value.reverse()
    byte_value = bytes(split_value)
    return byte_value.hex()


def hexStrToDec(input_value: str, reverse: bool = False) -> int:
    if RECLIST[ADDRTYPE.HEX].fullmatch(input_value):
        trimmed = input_value.lstrip('0xX')
        if len(trimmed) % 2:
            trimmed = '0' + trimmed
        byte_value = bytes.fromhex(trimmed)
        if reverse:
            byte_order = 'little'
        else:
            byte_order = 'big'
        return int.from_bytes(byte_value, byte_order)
    else:
        return -1


def hexStrToDecStr(hex_addr: str, reverse: bool = False) -> str:
    check_value = hexStrToDec(hex_addr, reverse)
    return '' if (check_value == -1) else str(check_value)


def isValidIPv4(input_value, addr_type: int = ADDRTYPE.NONE, strict: bool = False) -> bool:
    """
    Accepts string or int value and returns True if it is a value in the range of valid IPv4 addresses.
    The addr_type argument should be a value from the ADDRTYPE enum. If input is int you must use NONE or DEC addr_type.
    The string can be a dotted-quad format, hex format, or decimal format. (no leading or trailing whitespace)
    strict mode will require dotted-quad format to include four valid octets
    """
    check_value = -1

    if isinstance(input_value, str):
        if '.' in input_value and (addr_type in [ADDRTYPE.NONE, ADDRTYPE.DOTTED]):
            # Confirm match for dotted-quad format
            if len(input_value) <= 15 and IP_RECLIST[ADDRTYPE.DOTTED].fullmatch(input_value):
                if strict and not DOTTEDQUADIP_STRICTREC.fullmatch(input_value):
                    check_value = -2
                else:
                    check_value = 0
            else:
                check_value = -3
        elif IP_RECLIST[ADDRTYPE.DEC].fullmatch(input_value) and (addr_type in [ADDRTYPE.NONE, ADDRTYPE.DEC]):
            check_value = int(input_value)
        elif IP_RECLIST[ADDRTYPE.HEX].fullmatch(input_value) and (addr_type in [ADDRTYPE.NONE, ADDRTYPE.HEX]):
            check_value = int(input_value, 16)
    elif isinstance(input_value, int):
        if addr_type in [ADDRTYPE.NONE, ADDRTYPE.DEC]:
            check_value = input_value
        else:
            raise ValueError('Type int input_value passed with incompatible addr_type of {addr_type}')
    else:
        raise ValueError(f'Expected input type str or int. Got {type(input_value)}')

    return (check_value >= 0) and (check_value <= V4MAXVAL)
