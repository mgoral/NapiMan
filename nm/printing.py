# Copyright (C) 2016 Michał Góral.
#
# This file is part of NapiMan
#
# NapiMan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NapiMan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NapiMan. If not, see <http://www.gnu.org/licenses/>.

use_colors = True

def _colorize(s, c):
    if use_colors is True:
        ENDC = "\033[0m"
        return "%s%s%s" % (c, s, ENDC)
    return s

def green(s):
    return _colorize(s, "\033[92m")

def blue(s):
    return _colorize(s, "\033[94m")

def purple(s):
    return _colorize(s, "\033[95m")

def red(s):
    return _colorize(s, "\033[91m")

def bold(s):
    return _colorize(s, "\033[1m")

def underline(s):
    return _colorize(s, "\033[4m")

def use_colors(val):
    global use_colors
    use_colors = val
