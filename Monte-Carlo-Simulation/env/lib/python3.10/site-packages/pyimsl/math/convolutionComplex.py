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
from pyimsl.util.imslUtils import MATH, checkForBoolean, d_complex, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import dtype, shape
from ctypes import POINTER, byref, c_int

IMSL_PERIODIC = 10030
IMSL_CORRELATION = 11070
IMSL_FIRST_CALL = 11073
IMSL_CONTINUE_CALL = 11074
IMSL_LAST_CALL = 11075
imslmath = loadimsl(MATH)


def convolutionComplex(x, y, periodic=None, correlation=None, firstCall=None, continueCall=None, lastCall=None):
    imslmath.imsl_z_convolution.restype = POINTER(d_complex)
    shape = []
    evalstring = 'imslmath.imsl_z_convolution('
    evalstring += 'c_int(nx)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='d_complex', expectedShape=(0))
    evalstring += 'x'
    nx = shape[0]
    evalstring += ','
    evalstring += 'c_int(ny)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='d_complex', expectedShape=(0))
    evalstring += 'y'
    ny = shape[0]
    evalstring += ','
    nz_tmp = c_int()
    evalstring += 'byref(nz_tmp)'
    checkForBoolean(periodic, 'periodic')
    if (periodic):
        evalstring += ','
        evalstring += repr(IMSL_PERIODIC)
    checkForBoolean(correlation, 'correlation')
    if (correlation):
        evalstring += ','
        evalstring += repr(IMSL_CORRELATION)
    checkForBoolean(firstCall, 'firstCall')
    if (firstCall):
        evalstring += ','
        evalstring += repr(IMSL_FIRST_CALL)
    checkForBoolean(continueCall, 'continueCall')
    if (continueCall):
        evalstring += ','
        evalstring += repr(IMSL_CONTINUE_CALL)
    checkForBoolean(lastCall, 'lastCall')
    if (lastCall):
        evalstring += ','
        evalstring += repr(IMSL_LAST_CALL)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(nz_tmp), result=True)
