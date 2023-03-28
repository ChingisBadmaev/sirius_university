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
from numpy import double, dtype, gradient, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_GRADIENT = 10250
IMSL_PRINT = 10251
IMSL_XGUESS = 10100
IMSL_ITMAX = 10016
IMSL_TAU0 = 13001
IMSL_DEL0 = 13002
IMSL_SMALLW = 13003
IMSL_DELMIN = 13004
IMSL_SCFMAX = 13005
IMSL_OBJ = 10125
IMSL_DIFFTYPE = 13009
IMSL_XSCALE = 10106
IMSL_EPSDIF = 13006
IMSL_EPSFCN = 13007
IMSL_TAUBND = 13008
IMSL_FCN_W_DATA = 13101
IMSL_GRADIENT_W_DATA = 13102
IMSL_LAGRANGE_MULTIPLIERS = 11143
IMSL_CONSTRAINT_RESIDUALS = 14001

imslmath = loadimsl(MATH)


def constrainedNlp(fcn, m, meq, ibtype, xlb, xub, gradient=None, t_print=None, xguess=None, itmax=None,
                   tau0=None, del0=None, smallw=None, delmin=None, scfmax=None, obj=None, difftype=None, xscale=None,
                   epsdif=None, epsfcn=None, taubnd=None, lagrangeMultipliers=None, constraintResiduals=None):
    """ Solves a general nonlinear programming problem using a sequential equality constrained quadratic programming method.
    """
    imslmath.imsl_d_constrained_nlp.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_constrained_nlp('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_void_p, c_int, POINTER(c_double),
                        c_int, POINTER(c_double), POINTER(c_int))
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_int(m)'
    evalstring += ','
    evalstring += 'c_int(meq)'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(ibtype)'
    evalstring += ','
    xlb_tmp = toNumpyArray(xlb, 'xlb', shape=shape,
                           dtype='double', expectedShape=(0))
    evalstring += 'xlb_tmp.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    xub_tmp = toNumpyArray(xub, 'xub', shape=shape,
                           dtype='double', expectedShape=(n))
    evalstring += 'xub_tmp.ctypes.data_as(c_void_p)'
    if not (gradient is None):
        evalstring += ','
        evalstring += repr(IMSL_GRADIENT)
        evalstring += ','
        checkForCallable(gradient, 'gradient')
        TMP_GRADIENT_GRADIENT = CFUNCTYPE(
            c_void_p, c_int, POINTER(c_double), c_int, POINTER(c_double))
        tmp_gradient_gradient = TMP_GRADIENT_GRADIENT(gradient)
        evalstring += 'tmp_gradient_gradient'
    if not (t_print is None):
        evalstring += ','
        evalstring += repr(IMSL_PRINT)
        evalstring += ','
        evalstring += 'c_int(t_print)'
    if not (xguess is None):
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        xguess = toNumpyArray(xguess, 'xguess', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'xguess.ctypes.data_as(c_void_p)'
    if not (itmax is None):
        evalstring += ','
        evalstring += repr(IMSL_ITMAX)
        evalstring += ','
        evalstring += 'c_int(itmax)'
    if not (tau0 is None):
        evalstring += ','
        evalstring += repr(IMSL_TAU0)
        evalstring += ','
        evalstring += 'c_double(tau0)'
    if not (del0 is None):
        evalstring += ','
        evalstring += repr(IMSL_DEL0)
        evalstring += ','
        evalstring += 'c_double(del0)'
    if not (smallw is None):
        evalstring += ','
        evalstring += repr(IMSL_SMALLW)
        evalstring += ','
        evalstring += 'c_double(smallw)'
    if not (delmin is None):
        evalstring += ','
        evalstring += repr(IMSL_DELMIN)
        evalstring += ','
        evalstring += 'c_double(delmin)'
    if not (scfmax is None):
        evalstring += ','
        evalstring += repr(IMSL_SCFMAX)
        evalstring += ','
        evalstring += 'c_double(scfmax)'
    if not (obj is None):
        evalstring += ','
        evalstring += repr(IMSL_OBJ)
        checkForList(obj, 'obj')
        evalstring += ','
        obj_obj_tmp = c_double()
        evalstring += 'byref(obj_obj_tmp)'
    if not (difftype is None):
        evalstring += ','
        evalstring += repr(IMSL_DIFFTYPE)
        evalstring += ','
        evalstring += 'c_int(difftype)'
    if not (xscale is None):
        evalstring += ','
        evalstring += repr(IMSL_XSCALE)
        evalstring += ','
        xscale = toNumpyArray(xscale, 'xscale', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'xscale.ctypes.data_as(c_void_p)'
    if not (epsdif is None):
        evalstring += ','
        evalstring += repr(IMSL_EPSDIF)
        evalstring += ','
        evalstring += 'c_double(epsdif)'
    if not (epsfcn is None):
        evalstring += ','
        evalstring += repr(IMSL_EPSFCN)
        evalstring += ','
        evalstring += 'c_double(epsfcn)'
    if not (taubnd is None):
        evalstring += ','
        evalstring += repr(IMSL_TAUBND)
        evalstring += ','
        evalstring += 'c_double(taubnd)'
    if not (lagrangeMultipliers is None):
        evalstring += ','
        evalstring += repr(IMSL_LAGRANGE_MULTIPLIERS)
        checkForList(lagrangeMultipliers, 'lagrangeMultipliers')
        evalstring += ','
        lagrangeMultipliers_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(lagrangeMultipliers_tmp)'
    if not (constraintResiduals is None):
        evalstring += ','
        evalstring += repr(IMSL_CONSTRAINT_RESIDUALS)
        checkForList(constraintResiduals, 'constraintResiduals')
        evalstring += ','
        constraintResiduals_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(constraintResiduals_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (lagrangeMultipliers is None):
        processRet(lagrangeMultipliers_tmp, shape=(
            m), pyvar=lagrangeMultipliers)
    if not (constraintResiduals is None):
        processRet(constraintResiduals_tmp, shape=(
            m), pyvar=constraintResiduals)
    if isinstance(xlb, list):
        xlb[:] = []
    processRet(xlb_tmp, inout=True, shape=(n), pyvar=xlb)
    if isinstance(xub, list):
        xub[:] = []
    processRet(xub_tmp, inout=True, shape=(n), pyvar=xub)
    if not (obj is None):
        processRet(obj_obj_tmp, shape=1, pyvar=obj)
    return processRet(result, shape=(n), result=True)
