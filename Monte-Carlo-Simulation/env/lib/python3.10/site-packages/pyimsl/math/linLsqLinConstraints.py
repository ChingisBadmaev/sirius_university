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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSL_RESIDUAL = 10172
IMSL_PRINT = 10251
IMSL_MAX_ITER = 10305
IMSL_REL_FCN_TOL = 10110
IMSL_ABS_FCN_TOL = 10290
imslmath = loadimsl(MATH)


def linLsqLinConstraints(a, b, c, bl, bu, conType, xlb, xub, residual=None, t_print=None, maxIter=None, relFcnTol=None, absFcnTol=None):
    """ Solves a linear least-squares problem with linear constraints.
    """
    imslmath.imsl_d_lin_lsq_lin_constraints.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_lin_lsq_lin_constraints('
    evalstring += 'c_int(nra)'
    evalstring += ','
    evalstring += 'c_int(nca)'
    evalstring += ','
    evalstring += 'c_int(ncon)'
    evalstring += ','
    a = toNumpyArray(a, 'a', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'a.ctypes.data_as(c_void_p)'
    nra = shape[0]
    nca = shape[1]
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(nra))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    evalstring += ','
    c = toNumpyArray(c, 'c', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'c.ctypes.data_as(c_void_p)'
    ncon = shape[0]
    evalstring += ','
    bl = toNumpyArray(bl, 'bl', shape=shape,
                      dtype='double', expectedShape=(ncon))
    evalstring += 'bl.ctypes.data_as(c_void_p)'
    evalstring += ','
    bu = toNumpyArray(bu, 'bu', shape=shape,
                      dtype='double', expectedShape=(ncon))
    evalstring += 'bu.ctypes.data_as(c_void_p)'
    evalstring += ','
    conType = toNumpyArray(conType, 'conType', shape=shape,
                           dtype='int', expectedShape=(ncon))
    evalstring += 'conType.ctypes.data_as(c_void_p)'
    evalstring += ','
    xlb = toNumpyArray(xlb, 'xlb', shape=shape,
                       dtype='double', expectedShape=(nca))
    evalstring += 'xlb.ctypes.data_as(c_void_p)'
    evalstring += ','
    xub = toNumpyArray(xub, 'xub', shape=shape,
                       dtype='double', expectedShape=(nca))
    evalstring += 'xub.ctypes.data_as(c_void_p)'
    if not (residual is None):
        evalstring += ','
        evalstring += repr(IMSL_RESIDUAL)
        checkForList(residual, 'residual')
        evalstring += ','
        residual_residual_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(residual_residual_tmp)'
    checkForBoolean(t_print, 't_print')
    if (t_print):
        evalstring += ','
        evalstring += repr(IMSL_PRINT)
    if not (maxIter is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ITER)
        checkForList(maxIter, 'maxIter')
        evalstring += ','
        maxIter_maxIter_tmp = c_int()
        evalstring += 'byref(maxIter_maxIter_tmp)'
    if not (relFcnTol is None):
        evalstring += ','
        evalstring += repr(IMSL_REL_FCN_TOL)
        evalstring += ','
        evalstring += 'c_double(relFcnTol)'
    if not (absFcnTol is None):
        evalstring += ','
        evalstring += repr(IMSL_ABS_FCN_TOL)
        evalstring += ','
        evalstring += 'c_double(absFcnTol)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (residual is None):
        processRet(residual_residual_tmp, shape=(nra), pyvar=residual)
    if not (maxIter is None):
        processRet(maxIter_maxIter_tmp, shape=1, pyvar=maxIter)
    return processRet(result, shape=(nca), result=True)
