###########################################################################
# Copyright 2008-2019 Rogue Wave Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
###########################################################################


class ImslError (Exception):
    """ This class encapsulates information about an error that occurred
        during execution of a math/stat routine.
        An object of this class will be raised whenever an exceptional
        condition occurs during execution of the math/stat routine.
        For example:

        The error object contains two pieces of information:
        (1) type = The severity of the error, between 1 & 7
            severities are defined in imslUtils.h; for instance,
            IMSL_WARNING = 3
        (2) code = the (integer) error code
            Codes are defined in math/mathErrors.py and stat/statErrors.py
        (3) message = the string that describes the error code.
        try:
           callMathRoutine()
        except ImslError, e:
           print "Error occurred: ", e.type, " (", e.code, ") => ", e.str
    """

    def __init__(self, type, code, message):
        self.type = type
        self.code = code
        if (isinstance(message, bytes)):
            message = bytes.decode(message)
        self.args = message
        # Exception.message was depricated in Python 2.6 so we will do ourselves
        self.message = message

    def __str__(self):
        result = ""
        if (self.type is None):
            result += "None"
        else:
            result += repr(self.type)
        result += " ("
        if (self.code is None):
            result += "None"
        else:
            result += repr(self.code)
        result += "): "
        if (self.args is None):
            result += "None"
        else:
            result += self.args[0][:]
        return result
