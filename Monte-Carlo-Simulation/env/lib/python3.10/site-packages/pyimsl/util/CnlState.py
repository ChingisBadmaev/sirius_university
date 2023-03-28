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
# This class is an opaque wrapper for CNL (ctypes) state variables, which
# occur in a number of contexts.
#
# It provides methods and properties for getting the opaque state
# variable reference.  It also provides a dictionary to contain other
# related objects.
#
from pyimsl.util.CnlCtypesWrapper import CnlCtypesWrapper


class CnlState (CnlCtypesWrapper):
    def __init__(self, state):
        CnlCtypesWrapper.__init__(self, state)

    def getState(self):
        return self.getCtValue()

    def setState(self, state):
        self.setCtValue(state)

    state = property(getState, doc='Internal state reference')
