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
from pyimsl.util.VersionFacade import VersionFacade
from numpy import shape
from ctypes import POINTER, c_double
from .mathStructs import Imsl_d_mps

IMSL_NAME_RHS = 15003
IMSL_NAME_RANGES = 15004
IMSL_NAME_BOUNDS = 15005
IMSL_POSITIVE_INFINITY = 15006
IMSL_NEGATIVE_INFINITY = 15007
imslmath = loadimsl(MATH)


def readMps(filename, nameRhs=None, nameRanges=None, nameBounds=None, positiveInfinity=None, negativeInfinity=None):
    """ Reads an MPS file containing a linear programming problem or a quadratic programming problem.
    """
    VersionFacade.checkVersion(6)
    imslmath.imsl_d_read_mps.restype = POINTER(Imsl_d_mps)
    shape = []
    evalstring = 'imslmath.imsl_d_read_mps('
    checkForStr(filename, 'filename')
    evalstring += 'toByte(filename)'
    if not (nameRhs is None):
        evalstring += ','
        evalstring += repr(IMSL_NAME_RHS)
        evalstring += ','
        checkForStr(nameRhs, 'nameRhs')
        evalstring += 'toByte(nameRhs)'
    if not (nameRanges is None):
        evalstring += ','
        evalstring += repr(IMSL_NAME_RANGES)
        evalstring += ','
        checkForStr(nameRanges, 'nameRanges')
        evalstring += 'toByte(nameRanges)'
    if not (nameBounds is None):
        evalstring += ','
        evalstring += repr(IMSL_NAME_BOUNDS)
        evalstring += ','
        checkForStr(nameBounds, 'nameBounds')
        evalstring += 'toByte(nameBounds)'
    if not (positiveInfinity is None):
        evalstring += ','
        evalstring += repr(IMSL_POSITIVE_INFINITY)
        evalstring += ','
        evalstring += 'c_double(positiveInfinity)'
    if not (negativeInfinity is None):
        evalstring += ','
        evalstring += repr(IMSL_NEGATIVE_INFINITY)
        evalstring += ','
        evalstring += 'c_double(negativeInfinity)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
