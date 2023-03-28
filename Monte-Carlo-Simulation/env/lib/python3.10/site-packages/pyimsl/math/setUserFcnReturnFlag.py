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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *

imslmath = loadimsl(MATH)


def setUserFcnReturnFlag(code):
    """ Indicates a condition has occurred in a user-supplied function necessitating a return to the calling function.
    """
    imslmath.imsl_set_user_fcn_return_flag.restype = None
    shape = []
    evalstring = 'imslmath.imsl_set_user_fcn_return_flag('
    evalstring += 'c_int(code)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return
