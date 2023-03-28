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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_XGUESS = 10100
IMSL_GRAD = 10105
IMSL_XSCALE = 10106
IMSL_FSCALE = 10107
IMSL_GRAD_TOL = 10108
IMSL_STEP_TOL = 10109
IMSL_MAX_STEP = 10111
IMSL_GOOD_DIGIT = 10112
IMSL_MAX_ITN = 10113
IMSL_MAX_FCN = 10103
IMSL_MAX_GRAD = 10114
IMSL_INIT_HESSIAN = 10115
IMSL_FVALUE = 10116
IMSL_FCN_W_DATA = 13101
IMSL_GRADIENT_W_DATA = 13102
imslmath = loadimsl(MATH)


def minUnconMultivar(fcn, n, xguess=None, grad=None, xscale=None, fscale=None, gradTol=None, stepTol=None, maxStep=None, goodDigit=None, maxItn=None, maxFcn=None, maxGrad=None, initHessian=None, fvalue=None):
    """ Minimizes a function f(x) of n variables using a quasi-Newton method.
    """
    imslmath.imsl_d_min_uncon_multivar.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_min_uncon_multivar('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_int, POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(n)'
    if not (xguess is None):
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        xguess = toNumpyArray(xguess, 'xguess', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'xguess.ctypes.data_as(c_void_p)'
    if not (grad is None):
        evalstring += ','
        evalstring += repr(IMSL_GRAD)
        evalstring += ','
        checkForCallable(grad, 'grad')
        TMP_GRAD_GRAD = CFUNCTYPE(
            c_void_p, c_int, POINTER(c_double), POINTER(c_double))
        tmp_grad_grad = TMP_GRAD_GRAD(grad)
        evalstring += 'tmp_grad_grad'
    if not (xscale is None):
        evalstring += ','
        evalstring += repr(IMSL_XSCALE)
        evalstring += ','
        xscale = toNumpyArray(xscale, 'xscale', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'xscale.ctypes.data_as(c_void_p)'
    if not (fscale is None):
        evalstring += ','
        evalstring += repr(IMSL_FSCALE)
        evalstring += ','
        evalstring += 'c_double(fscale)'
    if not (gradTol is None):
        evalstring += ','
        evalstring += repr(IMSL_GRAD_TOL)
        evalstring += ','
        evalstring += 'c_double(gradTol)'
    if not (stepTol is None):
        evalstring += ','
        evalstring += repr(IMSL_STEP_TOL)
        evalstring += ','
        evalstring += 'c_double(stepTol)'
    if not (maxStep is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_STEP)
        evalstring += ','
        evalstring += 'c_double(maxStep)'
    if not (goodDigit is None):
        evalstring += ','
        evalstring += repr(IMSL_GOOD_DIGIT)
        evalstring += ','
        evalstring += 'c_int(goodDigit)'
    if not (maxItn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ITN)
        evalstring += ','
        evalstring += 'c_int(maxItn)'
    if not (maxFcn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_FCN)
        evalstring += ','
        evalstring += 'c_int(maxFcn)'
    if not (maxGrad is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_GRAD)
        evalstring += ','
        evalstring += 'c_int(maxGrad)'
    if not (initHessian is None):
        evalstring += ','
        evalstring += repr(IMSL_INIT_HESSIAN)
        evalstring += ','
        evalstring += 'c_int(initHessian)'
    if not (fvalue is None):
        evalstring += ','
        evalstring += repr(IMSL_FVALUE)
        checkForList(fvalue, 'fvalue')
        evalstring += ','
        fvalue_fvalue_tmp = c_double()
        evalstring += 'byref(fvalue_fvalue_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (fvalue is None):
        processRet(fvalue_fvalue_tmp, shape=1, pyvar=fvalue)
    return processRet(result, shape=(n), result=True)
