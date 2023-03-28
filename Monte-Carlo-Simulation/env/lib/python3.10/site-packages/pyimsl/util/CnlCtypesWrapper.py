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
# This class is an opaque wrapper for CNL (ctypes) variables, which
# occur in a number of contexts.
#
# It provides methods and properties for getting and setting the value.
#


class CnlCtypesWrapper (object):
    def __init__(self, ctValue):
        self.__ctValue__ = ctValue

    def getCtValue(self):
        return self.__ctValue__

    def setCtValue(self, ctValue):
        self.__ctValue__ = ctValue

    def getValue(self):
        if (self.__ctValue__ is None):
            return None
        else:
            return self.__ctValue__.value

    def setValue(self, value):
        self.__ctValue__.value = value

    value = property(fget=getValue, fset=setValue, doc='Variable value')
