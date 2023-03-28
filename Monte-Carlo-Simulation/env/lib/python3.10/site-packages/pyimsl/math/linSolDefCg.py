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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, shape, size
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_MAX_ITER = 10305
IMSL_REL_ERR = 10307
IMSL_PRECOND = 10306
IMSL_JACOBI = 10244
IMSL_FCN_W_DATA = 13101
IMSL_PRECOND_W_DATA = 13103
imslmath = loadimsl(MATH)


def linSolDefCg(amultp, b, maxIter=None, relErr=None, precond=None, jacobi=None, fcnWData=None, precondWData=None):
    """ Solves a real symmetric definite linear system using a conjugate gradient method. Using optional arguments, a preconditioner can be supplied.
    """
    imslmath.imsl_d_lin_sol_def_cg.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_lin_sol_def_cg('
    evalstring += 'c_int(n)'
    evalstring += ','
    checkForCallable(amultp, 'amultp')
    TMP_AMULTP = CFUNCTYPE(c_void_p, POINTER(c_double), POINTER(c_double))
    tmp_amultp = TMP_AMULTP(amultp)
    evalstring += 'tmp_amultp'
    evalstring += ','
    b = toNumpyArray(b, 'b', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'b.ctypes.data_as(c_void_p)'
    n = shape[0]
    if not (maxIter is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ITER)
        # checkForList(maxIter,'maxIter')
        evalstring += ','
        maxIter_maxit_tmp = maxIter[0]
        if (not(isinstance(maxIter_maxit_tmp, c_int))):
            maxIter_maxit_tmp = c_int(maxIter[0])
        evalstring += 'byref(maxIter_maxit_tmp)'
    if not (relErr is None):
        evalstring += ','
        evalstring += repr(IMSL_REL_ERR)
        evalstring += ','
        evalstring += 'c_double(relErr)'
    if not (precond is None):
        evalstring += ','
        evalstring += repr(IMSL_PRECOND)
        evalstring += ','
        checkForCallable(precond, 'precond')
        TMP_PRECOND_PRECOND = CFUNCTYPE(
            c_void_p, POINTER(c_double), POINTER(c_double))
        tmp_precond_precond = TMP_PRECOND_PRECOND(precond)
        evalstring += 'tmp_precond_precond'
    if not (jacobi is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBI)
        evalstring += ','
        jacobi = toNumpyArray(jacobi, 'jacobi', shape=shape,
                              dtype='double', expectedShape=(n))
        evalstring += 'jacobi.ctypes.data_as(c_void_p)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForList(fcnWData, 'fcnWData', size=2)
        evalstring += ','
        tmp_fcnWData_fcnWData_param = fcnWData[0]
        checkForCallable(tmp_fcnWData_fcnWData_param, 'fcnWData')
        TMP_FCNWDATA_FCNWDATA = CFUNCTYPE(c_void_p, POINTER(
            c_double), POINTER(c_double), POINTER(c_double))
        tmp_fcnWData_fcnWData = TMP_FCNWDATA_FCNWDATA(
            tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring += ','
        fcnWData_data_tmp = fcnWData[1]
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (precondWData is None):
        evalstring += ','
        evalstring += repr(IMSL_PRECOND_W_DATA)
        checkForList(precondWData, 'precondWData', size=2)
        evalstring += ','
        tmp_precondWData_precondWData_param = precondWData[0]
        checkForCallable(tmp_precondWData_precondWData_param, 'precondWData')
        TMP_PRECONDWDATA_PRECONDWDATA = CFUNCTYPE(
            c_void_p, POINTER(c_double), POINTER(c_double), POINTER(c_double))
        tmp_precondWData_precondWData = TMP_PRECONDWDATA_PRECONDWDATA(
            tmp_precondWData_precondWData_param)
        evalstring += 'tmp_precondWData_precondWData'
        evalstring += ','
        precondWData_data_tmp = precondWData[1]
        precondWData_data_tmp = toNumpyArray(
            precondWData_data_tmp, 'data', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'precondWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (maxIter is None):
        if isinstance(maxIter, list):
            maxIter[:] = []
        processRet(maxIter_maxit_tmp, shape=1, pyvar=maxIter)
    return processRet(result, shape=(n), result=True)
