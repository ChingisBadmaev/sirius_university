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
from numpy import double, dtype, shape, size, empty
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p

IMSL_TOL = 10072
IMSL_HINIT = 10073
IMSL_PRINT = 10251
IMSL_MAX_SUBINTER = 10021
IMSL_PROBLEM_EMBEDDED = 13111
IMSL_ERR_EST = 10020
IMSL_FCN_W_DATA = 13101
IMSL_JACOBIAN_W_DATA = 13104
IMSL_FCN_BC_W_DATA = 13108
IMSL_PROBLEM_EMBEDDED_W_DATA = 13113
imslmath = loadimsl(MATH)


def bvpFiniteDifference(fcneq, fcnjac, fcnbc, n, nleft, ncupbc, tleft, tright, linear, nfinal, tfinal, yfinal, tol=None, hinit=None, t_print=None, maxSubinter=None, problemEmbedded=None, errEst=None, fcnWData=None, jacobianWData=None, fcnBcWData=None, problemEmbeddedWData=None):
    """ Solves a (parameterized) system of differential equations with boundary conditions at two points, using a variable order, variable step size finite difference method with deferred corrections.
    """
    imslmath.imsl_d_bvp_finite_difference.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_bvp_finite_difference('
    checkForCallable(fcneq, 'fcneq')
    TMP_FCNEQ = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
        c_double), c_double, POINTER(c_double))
    tmp_fcneq = TMP_FCNEQ(fcneq)
    evalstring += 'tmp_fcneq'
    evalstring += ','
    checkForCallable(fcnjac, 'fcnjac')
    TMP_FCNJAC = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
        c_double), c_double, POINTER(c_double))
    tmp_fcnjac = TMP_FCNJAC(fcnjac)
    evalstring += 'tmp_fcnjac'
    evalstring += ','
    checkForCallable(fcnbc, 'fcnbc')
    TMP_FCNBC = CFUNCTYPE(c_void_p, c_int, POINTER(
        c_double), POINTER(c_double), c_double, POINTER(c_double))
    tmp_fcnbc = TMP_FCNBC(fcnbc)
    evalstring += 'tmp_fcnbc'
    evalstring += ','
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(nleft)'
    evalstring += ','
    evalstring += 'c_int(ncupbc)'
    evalstring += ','
    evalstring += 'c_double(tleft)'
    evalstring += ','
    evalstring += 'c_double(tright)'
    evalstring += ','
    evalstring += 'c_int(linear)'
    evalstring += ','
    nfinal_tmp = c_int()
    evalstring += 'byref(nfinal_tmp)'
    evalstring += ','
    mxgrid = 100
    if not (maxSubinter is None):
        mxgrid = maxSubinter
    tfinal_tmp = empty((mxgrid), dtype=double)
    evalstring += 'tfinal_tmp.ctypes.data_as(c_void_p)'
    evalstring += ','
    yfinal_tmp = empty((mxgrid, n), dtype=double)
    n_yfinal = len(yfinal_tmp[0])
    evalstring += 'yfinal_tmp.ctypes.data_as(c_void_p)'
    if not (tol is None):
        evalstring += ','
        evalstring += repr(IMSL_TOL)
        evalstring += ','
        evalstring += 'c_double(tol)'
    if not (hinit is None):
        evalstring += ','
        evalstring += repr(IMSL_HINIT)
        checkForDict(hinit, 'hinit', ['tinit', 'yinit'])
        evalstring += ','
        evalstring += 'c_int(hinit_ninit_tmp)'
        evalstring += ','
        hinit_tinit_tmp = hinit['tinit']
        hinit_tinit_tmp = toNumpyArray(
            hinit_tinit_tmp, 'tinit', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'hinit_tinit_tmp.ctypes.data_as(c_void_p)'
        hinit_ninit_tmp = shape[0]
        evalstring += ','
        hinit_yinit_tmp = hinit['yinit']
        hinit_yinit_tmp = toNumpyArray(
            hinit_yinit_tmp, 'yinit', shape=shape, dtype='double', expectedShape=(hinit_ninit_tmp, n))
        evalstring += 'hinit_yinit_tmp.ctypes.data_as(c_void_p)'
    if not (t_print is None):
        evalstring += ','
        evalstring += repr(IMSL_PRINT)
        evalstring += ','
        evalstring += 'c_int(t_print)'
    if not (maxSubinter is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_SUBINTER)
        evalstring += ','
        evalstring += 'c_int(maxSubinter)'
    if not (problemEmbedded is None):
        evalstring += ','
        evalstring += repr(IMSL_PROBLEM_EMBEDDED)
        checkForDict(problemEmbedded, 'problemEmbedded',
                     ['pistep', 'fcnpeq', 'fcnpbc'])
        evalstring += ','
        problemEmbedded_pistep_tmp = problemEmbedded['pistep']
        evalstring += 'c_double(problemEmbedded_pistep_tmp)'
        evalstring += ','
        tmp_problemEmbedded_fcnpeq_param = problemEmbedded['fcnpeq']
        checkForCallable(tmp_problemEmbedded_fcnpeq_param, 'fcnpeq')
        TMP_PROBLEMEMBEDDED_FCNPEQ = CFUNCTYPE(
            c_void_p, c_int, c_double, POINTER(c_double), c_double, POINTER(c_double))
        tmp_problemEmbedded_fcnpeq = TMP_PROBLEMEMBEDDED_FCNPEQ(
            tmp_problemEmbedded_fcnpeq_param)
        evalstring += 'tmp_problemEmbedded_fcnpeq'
        evalstring += ','
        tmp_problemEmbedded_fcnpbc_param = problemEmbedded['fcnpbc']
        checkForCallable(tmp_problemEmbedded_fcnpbc_param, 'fcnpbc')
        TMP_PROBLEMEMBEDDED_FCNPBC = CFUNCTYPE(c_void_p, c_int, POINTER(
            c_double), POINTER(c_double), c_double, POINTER(c_double))
        tmp_problemEmbedded_fcnpbc = TMP_PROBLEMEMBEDDED_FCNPBC(
            tmp_problemEmbedded_fcnpbc_param)
        evalstring += 'tmp_problemEmbedded_fcnpbc'
    if not (errEst is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_EST)
        checkForList(errEst, 'errEst')
        evalstring += ','
        errEst_errest_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(errEst_errest_tmp)'
    if not (fcnWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData, 'fcnWData', ['fcneq', 'data'])
        evalstring += ','
        tmp_fcnWData_fcneq_param = fcnWData['fcneq']
        checkForCallable(tmp_fcnWData_fcneq_param, 'fcneq')
        TMP_FCNWDATA_FCNEQ = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
            c_double), c_double, POINTER(c_double), POINTER(c_double))
        tmp_fcnWData_fcneq = TMP_FCNWDATA_FCNEQ(tmp_fcnWData_fcneq_param)
        evalstring += 'tmp_fcnWData_fcneq'
        evalstring += ','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(
            fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (jacobianWData is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBIAN_W_DATA)
        checkForDict(jacobianWData, 'jacobianWData', ['fcnjac', 'data'])
        evalstring += ','
        tmp_jacobianWData_fcnjac_param = jacobianWData['fcnjac']
        checkForCallable(tmp_jacobianWData_fcnjac_param, 'fcnjac')
        TMP_JACOBIANWDATA_FCNJAC = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
            c_double), c_double, POINTER(c_double), POINTER(c_double))
        tmp_jacobianWData_fcnjac = TMP_JACOBIANWDATA_FCNJAC(
            tmp_jacobianWData_fcnjac_param)
        evalstring += 'tmp_jacobianWData_fcnjac'
        evalstring += ','
        jacobianWData_data_tmp = jacobianWData['data']
        jacobianWData_data_tmp = toNumpyArray(
            jacobianWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'jacobianWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (fcnBcWData is None):
        evalstring += ','
        evalstring += repr(IMSL_FCN_BC_W_DATA)
        checkForDict(fcnBcWData, 'fcnBcWData', ['fcnbc', 'data'])
        evalstring += ','
        tmp_fcnBcWData_fcnbc_param = fcnBcWData['fcnbc']
        checkForCallable(tmp_fcnBcWData_fcnbc_param, 'fcnbc')
        TMP_FCNBCWDATA_FCNBC = CFUNCTYPE(c_void_p, c_int, POINTER(c_double), POINTER(
            c_double), c_double, POINTER(c_double), POINTER(c_double))
        tmp_fcnBcWData_fcnbc = TMP_FCNBCWDATA_FCNBC(tmp_fcnBcWData_fcnbc_param)
        evalstring += 'tmp_fcnBcWData_fcnbc'
        evalstring += ','
        fcnBcWData_data_tmp = fcnBcWData['data']
        fcnBcWData_data_tmp = toNumpyArray(
            fcnBcWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'fcnBcWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (problemEmbeddedWData is None):
        evalstring += ','
        evalstring += repr(IMSL_PROBLEM_EMBEDDED_W_DATA)
        checkForDict(problemEmbeddedWData, 'problemEmbeddedWData',
                     ['pistep', 'fcnpeq', 'data'])
        evalstring += ','
        problemEmbeddedWData_pistep_tmp = problemEmbeddedWData['pistep']
        evalstring += 'c_double(problemEmbeddedWData_pistep_tmp)'
        evalstring += ','
        tmp_problemEmbeddedWData_fcnpeq_param = problemEmbeddedWData['fcnpeq']
        checkForCallable(tmp_problemEmbeddedWData_fcnpeq_param, 'fcnpeq')
        TMP_PROBLEMEMBEDDEDWDATA_FCNPEQ = CFUNCTYPE(c_void_p, c_int, c_double, POINTER(
            c_double), c_double, POINTER(c_double), POINTER(c_double))
        tmp_problemEmbeddedWData_fcnpeq = TMP_PROBLEMEMBEDDEDWDATA_FCNPEQ(
            tmp_problemEmbeddedWData_fcnpeq_param)
        evalstring += 'tmp_problemEmbeddedWData_fcnpeq'
        evalstring += ','
        problemEmbeddedWData_data_tmp = problemEmbeddedWData['data']
        problemEmbeddedWData_data_tmp = toNumpyArray(
            problemEmbeddedWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'problemEmbeddedWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(nfinal_tmp, shape=(1), pyvar=nfinal)
    processRet(tfinal_tmp, inout=True, shape=(mxgrid), pyvar=tfinal)
    processRet(yfinal_tmp, inout=True, shape=(mxgrid, n), pyvar=yfinal)
    if not (errEst is None):
        processRet(errEst_errest_tmp, shape=(n), pyvar=errEst, inout=True)
    return result
