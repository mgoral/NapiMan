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

import os

from nm.util import abs_diff
from nm.printing import green, blue

class TimeInfo:
    def __init__(self):
        self.fps = None
        self.length = None

    def __str__(self):
        return "fps: %s, length: %s" % (green(self.fps), blue(self.length))

    def __sub__(self, other):
        new = TimeInfo()
        new.fps = abs_diff(self.fps, other.fps)
        new.length = abs_diff(self.length, other.length)
        return new

    def __lt__(self, other):
        return self.fps < other.fps or (self.fps == other.fps and self.length < other.length)

class PageInfo:
    def __init__(self):
        self.url = None
        self.name = None

    def __str__(self):
        return self.name

class SubInfo:
    def __init__(self):
        self.sub_hash = None
        self.name = None
        self.time_info = TimeInfo()

    def __str__(self):
        return "%s, %s" % (self.name, self.time_info)

class MovieInfo:
    def __init__(self):
        self.path = None
        self.time_info = TimeInfo()

    def __str__(self):
        return "%s, %s" % (os.path.basename(self.path), self.time_info)
