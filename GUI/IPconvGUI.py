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


import wx
import wx.adv
import wx.lib.agw.persist as pm
from .IPconvGUIbase import BaseConverterFrame, BaseSettingsFrame
from .resources import *


# ctrl-[A,C,V,X,Z], shift-insert
ctrl_ascii_chars = [
    wx.WXK_CONTROL_A, wx.WXK_CONTROL_C, wx.WXK_CONTROL_V, wx.WXK_CONTROL_X, wx.WXK_CONTROL_Z, wx.WXK_INSERT
]


class IPConverterFrame(BaseConverterFrame):
    def __init__(self, *args, **kwds):
        BaseConverterFrame.__init__(self, *args, **kwds)
        # Used for dragging implementation
        self._initial_position = None

        # Last selected text control is remembered for use with reverse checkbox callback
        self.last_selected = self.text_ctrl_hex

        self.settings_window = SettingsFrame(self, name='SettingsFrame')

        self.themes = {
            'dark': {
                'background': {'main': wx.Colour(60, 60, 60), 'text': wx.Colour(85, 85, 85)},
                'foreground': {'main': wx.Colour(192, 192, 192), 'text': wx.Colour(232, 232, 232)}
            },
            'light': {
                'background': {'main': wx.Colour(238, 238, 238), 'text': wx.Colour(255, 255, 255)},
                'foreground': {'main': wx.Colour(0, 0, 0), 'text': wx.Colour(0, 0, 0)}
            }
        }

        # Hotkey registration and binding
        # TODO: Check the return from RegisterHotKey
        # TODO: Identify why Win+Z wasn't working for me on Windows 10 (Ctrl-Win-Z works)
        self.RegisterHotKey(self.text_ctrl_hex.GetId(), wx.MOD_CONTROL | wx.MOD_META, ord('Z'))  # Ctrl-Win-Z
        self.Bind(wx.EVT_HOTKEY, self.on_paste, id=self.text_ctrl_hex.GetId())

        # Catching when the window transitions to/from being the active window the user is interacting with
        self.Bind(wx.EVT_ACTIVATE, self.on_activate)

        # Allow general handling of focus events for any relevant widget
        self.Bind(wx.EVT_CHILD_FOCUS, self.on_child_focus)

        # Allow 'minimizing' the window when pressing Escape if the frame has focus
        self.panel_main.Bind(wx.EVT_CHAR_HOOK, self.on_key)

        # Mouse bindings (for dragging the panel)
        self.panel_main.Bind(wx.EVT_LEFT_UP, self.on_mouse_button_up)
        self.panel_main.Bind(wx.EVT_MOTION, self.on_mouse)
        self.panel_main.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.on_mouse_lost)

        # Catching text input, used to automatically run conversions
        self.Bind(wx.EVT_TEXT, self.on_text, self.text_ctrl_dec)
        self.Bind(wx.EVT_TEXT, self.on_text, self.text_ctrl_dotted)
        self.Bind(wx.EVT_TEXT, self.on_text, self.text_ctrl_hex)

        # Catching individual character input, to only allow valid characters
        self.text_ctrl_dec.Bind(wx.EVT_CHAR, self.on_char)
        self.text_ctrl_dotted.Bind(wx.EVT_CHAR, self.on_char)
        self.text_ctrl_hex.Bind(wx.EVT_CHAR, self.on_char)

        self.text_ctrl_dec.Bind(wx.EVT_TEXT_PASTE, self.on_paste)
        self.text_ctrl_dotted.Bind(wx.EVT_TEXT_PASTE, self.on_paste)
        self.text_ctrl_hex.Bind(wx.EVT_TEXT_PASTE, self.on_paste)

        self.SetName('MainFrame')
        self.checkbox_reverse.SetName('checkbox_reverse')

        # TODO: Confirm behavior with multiple monitors, especially on non-Windows systems.
        self.Center()

        self.persistence_manager = pm.PersistenceManager.Get()
        self.persistence_manager.SetManagerStyle(pm.PM_DEFAULT_STYLE | pm.PM_PERSIST_CONTROL_VALUE)

        # Restore any saved selections and window placement
        self.persistence_manager.RegisterAndRestore(self)
        self.persistence_manager.RegisterAndRestoreAll(
            self, children=[
                self.checkbox_reverse, self.settings_window.checkbox_monitorclipboard,
                self.settings_window.checkbox_stayontop, self.settings_window.radio_box_theme
            ]
        )

        self.apply_theme(theme_name=self.settings_window.radio_box_theme.GetStringSelection())
        self.monitor_clipboard_start()
        self.stay_on_top(enable=self.settings_window.checkbox_stayontop.IsChecked())

    def apply_theme(self, theme_name: str):
        theme = self.themes.get(theme_name, None)
        if not theme:
            return  # TODO: consider raising an exception, especially if customization is introduced.

        # Main colors
        background_main = theme['background']['main']
        foreground_main = theme['foreground']['main']

        # Colors for TextCtrl objects
        background_text = theme['background']['text']
        foreground_text = theme['foreground']['text']

        self.checkbox_reverse.SetBackgroundColour(background_main)
        self.checkbox_reverse.SetForegroundColour(foreground_main)

        self.bitmap_button_settings.SetBackgroundColour(background_main)
        self.bitmap_button_exit.SetBackgroundColour(background_main)

        self.text_ctrl_dotted.SetBackgroundColour(background_text)
        self.text_ctrl_dotted.SetForegroundColour(foreground_text)
        self.text_ctrl_hex.SetBackgroundColour(background_text)
        self.text_ctrl_hex.SetForegroundColour(foreground_text)
        self.text_ctrl_dec.SetBackgroundColour(background_text)
        self.text_ctrl_dec.SetForegroundColour(foreground_text)

        self.label_dotted.SetBackgroundColour(background_main)
        self.label_dotted.SetForegroundColour(foreground_main)
        self.label_hex.SetBackgroundColour(background_main)
        self.label_hex.SetForegroundColour(foreground_main)
        self.label_dec.SetBackgroundColour(background_main)
        self.label_dec.SetForegroundColour(foreground_main)

        self.panel_main.SetBackgroundColour(background_main)
        self.panel_main.SetForegroundColour(foreground_main)

        self.Refresh()

    @staticmethod
    def get_clipboard_string() -> tuple:
        """Try to get text data from the clipboard and return a tuple indicating success and the text value"""
        clipboard_string = ''
        success = False
        text_data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
        if success:
            clipboard_string = text_data.GetText()
        return success, clipboard_string

    def monitor_clipboard(self):
        """Monitor the clipboard when this application does not have focus"""
        if self.settings_window.checkbox_monitorclipboard.IsChecked() and (not self.IsActive()):
            # Submit another run to start later
            self.monitor_clipboard_start()
            # Return the data, which should be used in a subclass
            return self.get_clipboard_string()
        else:
            return None, None

    def monitor_clipboard_start(self):
        """Submit a delayed call for monitoring. This is useful to allow event handlers to complete beforehand."""
        wx.CallLater(1000, self.monitor_clipboard)

    def on_activate(self, event):
        """This is triggered when the user changes focus between this application and others"""
        # Check for valid self in case window has been destroyed (avoids exception when closing the program)
        if self and self.settings_window:
            # Start monitoring clipboard if we're configured to and another application has focus
            if self.settings_window.checkbox_monitorclipboard.IsChecked() and (not event.GetActive()):
                self.monitor_clipboard_start()
        event.Skip()

    def on_button_exit(self, event):
        """Save window position and settings when the user presses the button to close the application"""
        self.persistence_manager.SaveAndUnregister()
        self.Close(force=True)

    def on_button_settings(self, event):
        """Open the settings window, or focus it if it's already open."""
        if self.settings_window.IsShown():
            self.settings_window.Raise()
        else:
            self.settings_window.Show()
        self.settings_window.CenterOnParent()
        self.settings_window.checkbox_monitorclipboard.SetFocus()

    def on_char(self, event):
        """Allow movement and command keys in TextCtrl objects"""
        if event.IsKeyInCategory(wx.WXK_CATEGORY_NAVIGATION | wx.WXK_CATEGORY_CUT | wx.WXK_CATEGORY_TAB):
            event.Skip()
        elif event.GetKeyCode() in ctrl_ascii_chars:
            event.Skip()

    def on_checkbox_reverse(self, event):
        print("Event handler 'on_checkbox_reverse' not implemented!")
        event.Skip()

    def on_child_focus(self, event):
        """Allows general handling of focus events for different types of widgets throughout the program"""
        event_object = event.GetEventObject()
        if isinstance(event_object, wx.TextCtrl):
            if event_object in [self.text_ctrl_dotted, self.text_ctrl_hex, self.text_ctrl_dec]:
                self.last_selected = event_object
            wx.CallAfter(event_object.SetInsertionPointEnd)
            wx.CallAfter(event_object.SelectAll)
        else:
            event.Skip()

    def on_key(self, event):
        """Minimize (iconize) the window on escape key"""
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Iconize()
        else:
            event.Skip()

    def on_mouse(self, event):
        """Implement click-and-drag for the frame/panel"""
        if not event.Dragging():
            # Panel is not being dragged, reset and bail
            self._initial_position = None
            return
        if not self.panel_main.HasCapture():
            # In Drag event, make sure we capture the mouse
            self.panel_main.CaptureMouse()
        if not self._initial_position:
            # Panel is being dragged, store current position
            self._initial_position = event.GetPosition()
        else:
            # Panel is being dragged and we already have a previous position, move the window
            new_position = event.GetPosition()
            delta = self._initial_position - new_position
            self.SetPosition(self.GetPosition() - delta)

    def on_mouse_button_up(self, event):
        """Makes sure the mouse gets released from dragging"""
        if self.panel_main.HasCapture():
            self.panel_main.ReleaseMouse()

    def on_mouse_lost(self, event):
        """This function can be used to abort anything relying on mouse input."""
        pass

    def on_paste(self, event) -> tuple:
        """This will get the value from the clipboard and return a success indicator and string in a tuple"""
        return self.get_clipboard_string()

    def on_text(self, event):
        print("Event handler 'on_text' not implemented!")
        event.Skip()

    def stay_on_top(self, enable: bool = True):
        if enable:
            # Binary OR wx.STAY_ON_TOP to add it if it's not already present
            self.SetWindowStyle(self.GetWindowStyle() | wx.STAY_ON_TOP)
        else:
            # Binary XOR wx.STAY_ON_TOP to remove it if it is present
            self.SetWindowStyle(self.GetWindowStyle() ^ wx.STAY_ON_TOP)


class SettingsFrame(BaseSettingsFrame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0)
        BaseSettingsFrame.__init__(self, *args, **kwds)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.checkbox_monitorclipboard.SetName('checkbox_monitorclipboard')
        self.checkbox_stayontop.SetName('checkbox_stayontop')
        self.radio_box_theme.SetName('radio_box_theme')

    def on_about(self, event):
        program_description = \
            """Quick IP Converter can convert IPv4 addresses between dotted-quad, decimal and hexadecimal notation."""
        program_license = \
            "LGPL-3.0-or-later (GNU Lesser General Public License 3.0 or later)\n" \
            "See the files COPYING and COPYING.LESSER distributed with this program\n" \
            "or https://www.gnu.org/licenses/ if you did not receive them with your copy."
        info = wx.adv.AboutDialogInfo()
        info.SetIcon(IPconvPNG.GetIcon())
        info.SetName('Quick IP Converter')
        info.SetVersion('2.0')
        info.SetDescription(program_description)
        info.SetCopyright('(C) 2014, 2018 Brandon M. Pace <brandonmpace@gmail.com>')
        info.SetWebSite('https://github.com/brandonmpace/Quick-IP-Converter')
        info.SetLicense(program_license)
        # info.AddDeveloper('Brandon M. Pace')

        wx.adv.AboutBox(info, parent=self)

    def on_checkbox_monitorclipboard(self, event):
        if event.IsChecked():
            self.Parent.monitor_clipboard_start()
        event.Skip()

    def on_checkbox_stayontop(self, event):
        self.Parent.stay_on_top(event.IsChecked())
        event.Skip()

    def on_close(self, event):
        """This function is used to just hide the settings window when the user clicks the close button."""
        if event.CanVeto():
            self.Hide()
            event.Veto()
        else:
            event.Skip()

    def on_radiobox_theme(self, event):
        self.Parent.apply_theme(event.GetString())
        event.Skip()
