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


import GUI
import libIPconv as conv
import wx


class MainFrame(GUI.IPConverterFrame):
    def __init__(self, *args, **kwds):
        GUI.IPConverterFrame.__init__(self, *args, **kwds)
        self.last_changed = self.text_ctrl_hex
        self.text_ctrl_dec.addr_type = conv.ADDRTYPE.DEC
        self.text_ctrl_dotted.addr_type = conv.ADDRTYPE.DOTTED
        self.text_ctrl_hex.addr_type = conv.ADDRTYPE.HEX

        main_converter.register_callback(self.text_ctrl_dec.ChangeValue, conv.ADDRTYPE.DEC)
        main_converter.register_callback(self.text_ctrl_dotted.ChangeValue, conv.ADDRTYPE.DOTTED)
        main_converter.register_callback(self.text_ctrl_hex.ChangeValue, conv.ADDRTYPE.HEX)

        main_converter.reverse = self.checkbox_reverse.IsChecked()

    def monitor_clipboard(self):
        success, clipboard_content = super().monitor_clipboard()
        if success and clipboard_content:
            trimmed = clipboard_content.strip()
            if conv.RECLIST[conv.ADDRTYPE.HEX].fullmatch(trimmed) and (trimmed != self.text_ctrl_hex.GetValue()):
                self.text_ctrl_hex.SetValue(trimmed)
            elif conv.DOTTEDQUADIP_STRICTREC.fullmatch(trimmed) and (trimmed != self.text_ctrl_dotted.GetValue()):
                self.text_ctrl_dotted.SetValue(trimmed)

    def on_checkbox_reverse(self, event):
        main_converter.reverse = event.IsChecked()
        main_converter.set_value(self.last_selected.GetValue(), self.last_selected.addr_type)

    def on_char(self, event):
        super().on_char(event)

        if event.GetSkipped():
            return  # return if the key was already allowed

        event_control = event.GetEventObject()
        event_key = event.GetKeyCode()

        if conv.filters.isAllowedASCII(event_key, event_control.addr_type):
            event.Skip()
            if event_control.addr_type == conv.ADDRTYPE.DOTTED:
                control_content = event_control.GetValue()
                control_selection = event_control.GetSelection()

                # Insert the new character at the insertion point, over-writing any selected characters
                first = control_content[0:control_selection[0]]
                last = control_content[control_selection[1]:]
                check_value = first + chr(event_key) + last

                if event.GetSkipped():
                    if '.' not in check_value:
                        check_value += '.'
                    if check_value.endswith('.'):
                        check_value += '0'
                    if not conv.isValidIPv4(check_value, conv.ADDRTYPE.DOTTED):
                        event.Skip(False)
            else:
                event.Skip()

    def on_paste(self, event):
        success, pasted_string = super().on_paste(event)

        event_object = event.GetEventObject()

        filtered_string = conv.filters.filterChars(pasted_string, event_object.addr_type)
        if not filtered_string:
            return  # nothing to insert

        control_content = event_object.GetValue()
        control_selection = event_object.GetSelection()

        # Insert the new string at the insertion point, over-writing any selected characters
        first = control_content[0:control_selection[0]]
        last = control_content[control_selection[1]:]
        final_value = first + filtered_string + last

        event_object.SetValue(final_value)
        event_object.SetInsertionPoint(len(first + filtered_string))

    def on_text(self, event):
        event_object = event.GetEventObject()
        main_converter.set_value(event_object.GetValue(), event_object.addr_type)
        self.last_changed = event_object


class MainApp(wx.App):
    def OnInit(self):
        self.frame_main = MainFrame(None, wx.ID_ANY, "", name='MainFrame')
        self.SetTopWindow(self.frame_main)
        self.frame_main.Show()
        return True


if __name__ == "__main__":
    main_converter = conv.Converter()
    app = MainApp(0)
    app.MainLoop()
