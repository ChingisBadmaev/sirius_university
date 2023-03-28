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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, processRet
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_XGUESS = 10100
IMSL_ERR_REL = 10011
IMSL_GRAD_TOL = 10108
IMSL_MAX_FCN = 10103
IMSL_FVALUE = 10116
IMSL_GVALUE = 10117
IMSL_FCN_W_DATA = 13101
IMSL_GRADIENT_W_DATA = 13102
imslmath = loadimsl(MATH)


def minUnconDeriv(fcn, grad, a, b, xguess=None, errRel=None, gradTol=None, maxFcn=None, fvalue=None, gvalue=None):
    """ Finds the minimum point of a smooth function f(x) of a single variable using both function and first derivative evaluations.
    """
    imslmath.imsl_d_min_uncon_deriv.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_min_uncon_deriv('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    checkForCallable(grad, 'grad')
    TMP_GRAD = CFUNCTYPE(c_double, c_double)
    tmp_grad = TMP_GRAD(grad)
    evalstring += 'tmp_grad'
    evalstring += ','
    evalstring += 'c_double(a)'
    evalstring += ','
    evalstring += 'c_double(b)'
    if not (xguess is None):
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        evalstring += 'c_double(xguess)'
    if not (errRel is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_REL)
        evalstring += ','
        evalstring += 'c_double(errRel)'
    if not (gradTol is None):
        evalstring += ','
        evalstring += repr(IMSL_GRAD_TOL)
        evalstring += ','
        evalstring += 'c_double(gradTol)'
    if not (maxFcn is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_FCN)
        evalstring += ','
        evalstring += 'c_int(maxFcn)'
    if not (fvalue is None):
        evalstring += ','
        evalstring += repr(IMSL_FVALUE)
        checkForList(fvalue, 'fvalue')
        evalstring += ','
        fvalue_fvalue_tmp = c_double()
        evalstring += 'byref(fvalue_fvalue_tmp)'
    if not (gvalue is None):
        evalstring += ','
        evalstring += repr(IMSL_GVALUE)
        checkForList(gvalue, 'gvalue')
        evalstring += ','
        gvalue_gvalue_tmp = c_double()
        evalstring += 'byref(gvalue_gvalue_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (fvalue is None):
        processRet(fvalue_fvalue_tmp, shape=1, pyvar=fvalue)
    if not (gvalue is None):
        processRet(gvalue_gvalue_tmp, shape=1, pyvar=gvalue)
    return result
