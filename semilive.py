# Copyright (c) 2017, Brandon Jones.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sublime
import sublime_plugin

g_counter = 0
g_playing = False
settings = sublime.load_settings("semilive.sublime-settings")

class SemiliveResetCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    global g_counter
    global g_playing
    g_counter = 0
    g_playing = False

class SemiliveNextCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    global g_counter
    global g_playing
    global settings

    if g_playing:
      return

    # "Lock" the command so that an accidental double-tap of the shortcut key
    # doesn't end up with two lines being typed over eachother simultaneously.
    g_playing = True

    playback_speed = 15

    script = settings.get("script", [])

    if (g_counter < len(script)):
      script_step = script[g_counter]
      g_counter += 1

      # Treat single script step as a list of one.
      if not isinstance(script_step, list):
        script_step = [ script_step ]

      t = 0

      highlight_lines = []

      for step_command in script_step:
        replace = step_command.get("replace", None)
        after = step_command.get("after", replace)
        instant = step_command.get("instant", False)
        highlight = step_command.get("highlight", True)
        insert_strings = step_command.get("insert", "")

        # Treat single insert string as a list of one.
        if not isinstance(insert_strings, list):
          insert_strings = [ insert_strings ]

        # All of the following insanity is because we want the characters to be
        # "typed" one-by-one. If we were OK with an instant insert this entire
        # section could be replaced with ~3 lines.
        def set_insertion_point(after, replace):
          def clear_and_set_point(after, replace):
            self.view.sel().clear()

            if not after and not replace:
              self.view.sel().add(sublime.Region(0, 0))

            if after:
              region = self.view.find(after, 0, sublime.LITERAL)
              if region:
                if replace:
                  self.view.sel().add(region)
                else:
                  self.view.sel().add(sublime.Region(region.end(), region.end()))
                  self.view.run_command('insert', {'characters': '\n'})
          return lambda: clear_and_set_point(after, replace)

        sublime.set_timeout(set_insertion_point(after, replace), t)
        t += playback_speed

        def insert_chars_cmd(str_chars):
          return lambda: self.view.run_command('insert', {'characters': str_chars})

        line_count = 0
        for insert_string in insert_strings:
          if highlight:
            highlight_lines.append(insert_string);
          line_count += 1
          if (line_count > 1):
            sublime.set_timeout(insert_chars_cmd('\n'), t)
            t += playback_speed
          if instant:
            sublime.set_timeout(insert_chars_cmd(insert_string), t)
            t += playback_speed
          else:
            for str_char in insert_string:
              sublime.set_timeout(insert_chars_cmd(str_char), t)
              if str_char == '\n':
                line_count += 1
              t += playback_speed
      # /end typing insanity

      # Highlight the text after we've typed it.
      def highlight_region(lines):
        def really_highlight_region(lines):
          for line in lines:
            if not line == '':
              self.view.run_command('semilive_highlight_internal', {'line': line})
        return lambda: really_highlight_region(lines)

      sublime.set_timeout(highlight_region(highlight_lines), t)
      t += playback_speed

      # "Unlock" the command when we're done typing so we can advanced to the
      # next step
      def unlock_plugin():
        global g_playing
        g_playing = False

      sublime.set_timeout(unlock_plugin, t)

class SemiliveHighlightInternalCommand(sublime_plugin.TextCommand):
  def run(self, edit, line='~~~'):
    region = self.view.find(line, 0, sublime.LITERAL)
    self.view.sel().add(region)

def plugin_loaded():
    global g_counter
    global g_playing
    global settings
    g_counter = 0
    g_playing = False
    settings = sublime.load_settings("semilive.sublime-settings")
