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

import re

from nm.util import nm_assert

class Time:
    # Yeah, I copied most of things here from Subconvert. Because why not?
    def __init__(self, time_string=None, seconds=None):
        if seconds is None and time_string is not None:
            self.__from_str(time_string)
        elif seconds is not None and time_string is None:
            self.__from_int(float(seconds))

    def __from_int(self, seconds):
        if seconds >= 0:
            self._full_seconds = seconds
        else:
            raise ValueError("Incorrect seconds value.")

        self._hours = int(seconds / 3600)
        seconds = round(seconds - self._hours * 3600, 3)
        self._minutes = int(seconds / 60)
        seconds = round(seconds - self._minutes * 60, 3)
        self._seconds = int(seconds)
        self._miliseconds = int(round(1000 * (seconds - self._seconds)))

    def __from_str(self, value):
        time = re.match(
            r"(?P<h>\d+):(?P<m>[0-5][0-9]):(?P<s>[0-5][0-9])(?:$|\.(?P<ms>\d{1,3}))", value)

        if time is None:
            raise ValueError("Incorrect time format.")

        if time.group('ms') is not None:
            # ljust explenation:
            # 10.1 != 10.001
            # 10.1 == 10.100
            self._miliseconds = int(time.group('ms').ljust(3, '0'))
        else:
            self._miliseconds = 0
        self._seconds = int(time.group('s'))
        self._minutes = int(time.group('m'))
        self._hours = int(time.group('h'))
        self._full_seconds = (3600*self._hours + 60*self._minutes + self._seconds + float(self._miliseconds)/1000)

    def __str__(self):
        return "%s:%s:%s.%s" % (self._hours, self._minutes, self._seconds, self._miliseconds)

    def __sub__(self, other):
        nm_assert(self._full_seconds >= other._full_seconds,
            "Cannot substract higher time from lower")

        result = self._full_seconds - other._full_seconds
        return Time(seconds = result)

    def __lt__(self, other):
        return self._full_seconds < other._full_seconds

    def __gt__(self, other):
        return self._full_seconds > other._full_seconds
