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
from pyimsl.util.imslUtils import MATH, checkForStr, fatalErrorCheck, loadimsl, toByte
from numpy import shape
from ctypes import c_double

imslmath = loadimsl(MATH)


def constant(name, unit=None):
    """ Returns the value of various mathematical and physical constants.
    """
    imslmath.imsl_d_constant.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_constant('
    checkForStr(name, 'name')
    evalstring += 'toByte(name)'
    if not (unit is None):
        checkForStr(unit, 'unit')
        evalstring += ','
        evalstring += 'toByte(unit)'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
