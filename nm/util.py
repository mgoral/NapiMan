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

class ErrorCode:
    NO_ERROR = 0
    FATAL_ERROR = 1
    BAD_INPUT = 2
    ASSERTION = 3

class ExceptionWithCode(Exception):
    def __init__(self, code, description = None):
        super().__init__(code, description)

    def error_code(self):
        return self.args[0]

    def description(self):
        return self.args[1]

    def __str__(self):
        if self.description() is None:
            return str()
        return str(self.description())

def nm_assert(val, desc = None, code = ErrorCode.ASSERTION):
    if not val:
        raise ExceptionWithCode(code, desc)

def abs_diff(lhs, rhs):
    if lhs < rhs:
        return rhs - lhs
    else:
        return lhs - rhs
