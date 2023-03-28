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

IMSL_EQ_ORDER = 13116
IMSL_EQ_ERR = 13117
IMSL_STEPSIZE_INC = 13120
IMSL_STEPSIZE_DEC = 13118
IMSL_MIN_STEPSIZE = 13122
IMSL_MAX_STEPSIZE = 15068
imslmath = loadimsl(MATH)


def odeAdamsKrogh(neq, t, tend, ido, y, hidrvs, fcn, eqOrder=None, eqErr=None, stepsizeInc=None, stepsizeDec=None, minStepsize=None, maxStepsize=None):
    imslmath.imsl_d_ode_adams_krogh.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_ode_adams_krogh('
    evalstring += 'c_int(neq)'
    evalstring += ','
    t_tmp = t[0]
    if (not(isinstance(t_tmp, c_double))):
        t_tmp = c_double(t[0])
    evalstring += 'byref(t_tmp)'
    evalstring += ','
    evalstring += 'c_double(tend)'
    evalstring += ','
    ido_tmp = ido[0]
    if (not(isinstance(ido_tmp, c_int))):
        ido_tmp = c_int(ido[0])
    evalstring += 'byref(ido_tmp)'
    evalstring += ','
    # Custom code.  Need to calculate expected length of y.
    k = 0
    if not (eqOrder is None):
        for i in range(neq):
            k += eqOrder[i]
    else:
        k = neq
    y_tmp = toNumpyArray(y, 'y', shape=shape,
                         dtype='double', expectedShape=(k))
    evalstring += 'y_tmp.ctypes.data_as(c_void_p)'
    evalstring += ','
    # Custom code.  hidrvs is a required argument that is output and may
    # be empty on input.
    hidrvs_tmp = empty(neq, dtype='double')
    evalstring += 'hidrvs_tmp.ctypes.data_as(c_void_p)'
    # hidrvs_tmp = POINTER(c_double)(c_double())
    # evalstring += 'byref(hidrvs_tmp)'
    evalstring += ','
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(None, c_int, c_int, c_double,
                        POINTER(c_double), POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    if not (eqOrder is None):
        evalstring += ','
        evalstring += repr(IMSL_EQ_ORDER)
        evalstring += ','
        eqOrder = toNumpyArray(
            eqOrder, 'eqOrder', shape=shape, dtype='int', expectedShape=(neq))
        evalstring += 'eqOrder.ctypes.data_as(c_void_p)'
    if not (eqErr is None):
        evalstring += ','
        evalstring += repr(IMSL_EQ_ERR)
        evalstring += ','
        eqErr = toNumpyArray(eqErr, 'eqErr', shape=shape,
                             dtype='double', expectedShape=(neq))
        evalstring += 'eqErr.ctypes.data_as(c_void_p)'
    if not (stepsizeInc is None):
        evalstring += ','
        evalstring += repr(IMSL_STEPSIZE_INC)
        evalstring += ','
        evalstring += 'c_double(stepsizeInc)'
    if not (stepsizeDec is None):
        evalstring += ','
        evalstring += repr(IMSL_STEPSIZE_DEC)
        evalstring += ','
        evalstring += 'c_double(stepsizeDec)'
    if not (minStepsize is None):
        evalstring += ','
        evalstring += repr(IMSL_MIN_STEPSIZE)
        evalstring += ','
        evalstring += 'c_double(minStepsize)'
    if not (maxStepsize is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_STEPSIZE)
        evalstring += ','
        evalstring += 'c_double(maxStepsize)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(t_tmp, inout=True, shape=(1), pyvar=t)
    processRet(ido_tmp, inout=True, shape=(1), pyvar=ido)
    processRet(y_tmp, inout=True, shape=(k), pyvar=y)
    # avoid emptying out hidrvs when ido = 3.
    if (ido[0] != 3):
        processRet(hidrvs_tmp, shape=(neq), pyvar=hidrvs)
    return
