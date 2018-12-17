# Quick IP Converter

Copyright (C) 2014, 2018 Brandon M. Pace <brandonmpace@gmail.com>

License: LGPL-3.0-or-later

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this program.
    If not, see <https://www.gnu.org/licenses/>.

Convert values between decimal, hexadecimal and dotted-quad IP formats

Dotted Quad accepts IPv4 addresses or subnet masks in the following formats:

    - 192.168.10.1
    - 255.255.240.0

Hex accepts hex values with optional 0x or 0X prefix:

    - 0xc0a80101
    - 0X0A0A0A01
    - 1bb

Decimal will accept any valid decimal value with no separators:

    - 123
    - 23456

**Notes:**

    - The clipboard monitoring action only runs when the application does not have focus.
    - 2.0 release removed most hotkeys
    - Reverse checkbox triggers conversion from the last selected text box


**Revision history:**

    2.0: Completely new GUI that is smaller in size
        - Removed IP checkbox
        - Removed About button
        - Added option to monitor clipboard for hex or dotted quad values once a second and automatically run conversion
            - The clipboard is only monitored when another application has focus.
        - Allow for much larger numbers for decimal-hex conversion
        - All hotkeys removed except for Ctrl-Win-Z, which will take a hex value from the clipboard and run conversion
        - Added a settings window, which contains the About link
        - Added option for dark theme
        - Added option to disable 'stay on top'
        - Reverse option is now true byte-order flip for all conversions
        - Reverse checkbox now triggers conversion from the last selected TextCtrl
        - Paste now works properly instead of replacing the entire contents of the TextCtrl
        - Window position and settings are saved when the exit button in the window is clicked

    1.8: Updated to use Python 3.6.5 and wxPython Phoenix 4.0.3
        - Pressing Enter is no longer necessary to trigger calculation. You can type or paste values and calculation will automatically run.
        - Clicking inside of a text box now selects all text if it wasn't already in focus.
            - The text is not copied to the clipboard in case you are trying to paste current clipboard data in the same place.
        - Each text box now only allows relevant characters to be placed there.
        - Limitation: The largest decimal number supported is 18446744073709551615 (8 bytes, hex ffffffffffffffff)

    1.6: Further enhancements to facilitate keyboard-only use. (even with the window not in focus, so these are Global)
        - Added keyboard shortcuts that process data from the Windows clipboard and toggle the IP/Reverse checkboxes as needed: (Thanks goes to Dan Cross for the recommendation)
            - Win + Z = Process Hex IP (enables IP)
            - Win + X = Process Dotted-Quad IP (enables IP)
            - Ctrl + Win + Z = Process Hex to Decimal
            - Ctrl + Win + X = Process Decimal to Hex
            - Win + A = Toggle Reverse
            
        If IP is unchecked and Reverse gets checked, both will get selected.
        If IP and Reverse are both checked, and IP gets unchecked, both will get deselected.
        

    1.4: Focus was on user experience and allowing keyboard-only use:
        - Removed buttons. Input is now processed upon pressing 'Enter'
        - Added conversion to Decimal IP.
        - Background color normalized
        - Using the 'Tab' key to traverse the window is now enabled.

    1.2:
        - Added 'IP' checkbox to allow for non-IP conversion between decimal-hex.

    1.0:
        - Initial release with decimal-hex conversion and reverse option.
