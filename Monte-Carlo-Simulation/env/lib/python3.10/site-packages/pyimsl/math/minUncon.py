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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForDict, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, c_double, c_int, c_void_p

IMSL_XGUESS = 10100
IMSL_STEP = 10101
IMSL_ERR_ABS = 10010
IMSL_MAX_FCN = 10103
IMSL_FCN_W_DATA = 13101
imslmath = loadimsl(MATH)


def minUncon(fcn, a, b, xguess=None, step=None, errAbs=None, maxFcn=None):
    """ Find the minimum point of a smooth function f(x) of a single variable using only function evaluations.
    """
    imslmath.imsl_d_min_uncon.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_min_uncon('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_double(a)'
    evalstring += ','
    evalstring += 'c_double(b)'
    if not (xguess is None):
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        evalstring += 'c_double(xguess)'
    if not (step is None):
        evalstring += ','
        evalstring += repr(IMSL_STEP)
        evalstring += ','
        evalstring += 'c_double(step)'
    if not (errAbs is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_ABS)
        evalstring += ','
        evalstring += 'c_double(errAbs)'
    if not (maxFcn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_FCN)
        evalstring += ','
        evalstring += 'c_int(maxFcn)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
