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

IMSL_N_CONSTRAINTS = 15061
IMSL_JACOBIAN_OPTION = 15062
IMSL_YPRIME_METHOD = 15063
IMSL_JACOBIAN_MATRIX_TYPE = 15064
IMSL_METHOD = 10309
IMSL_N_LOWER_DIAG = 15065
IMSL_N_UPPER_DIAG = 15066
IMSL_RELATIVE_TOLERANCE = 14041
IMSL_ABSOLUTE_TOLERANCE = 14042
IMSL_INITIAL_STEPSIZE = 11137
IMSL_MAX_STEPSIZE = 15068
IMSL_MAX_ORDER = 15070
IMSL_MAX_NUMBER_STEPS = 10077
IMSL_INTEGRATION_LIMIT = 15071
IMSL_ORDER_MAGNITUDE_EST = 15073
IMSL_GCN_W_DATA = 13100
imslmath = loadimsl(MATH)


def differentialAlgebraicEqs(t, tend, ido, y, yprime, gcn, nConstraints=None, jacobianOption=None, yprimeMethod=None, jacobianMatrixType=None, method=None, nLowerDiag=None, nUpperDiag=None, relativeTolerance=None, absoluteTolerance=None, initialStepsize=None, maxStepsize=None, maxOrder=None, maxNumberSteps=None, integrationLimit=None, orderMagnitudeEst=None):
    """ Solves a first order differential-algebraic system of equations, g(t, y, y') = 0, with optional additional constraints and user-defined linear system solver.
    """
    imslmath.imsl_d_differential_algebraic_eqs.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_differential_algebraic_eqs('
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
    y_tmp = toNumpyArray(y, 'y', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'y_tmp.ctypes.data_as(c_void_p)'
    neq = shape[0]
    evalstring += ','
    yprime_tmp = toNumpyArray(
        yprime, 'yprime', shape=shape, dtype='double', expectedShape=(neq))
    evalstring += 'yprime_tmp.ctypes.data_as(c_void_p)'
    evalstring += ','
    checkForCallable(gcn, 'gcn')
    TMP_GCN = CFUNCTYPE(None, c_int, c_double, POINTER(c_double), POINTER(
        c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_int))
    tmp_gcn = TMP_GCN(gcn)
    evalstring += 'tmp_gcn'
    if not (nConstraints is None):
        evalstring += ','
        evalstring += repr(IMSL_N_CONSTRAINTS)
        evalstring += ','
        evalstring += 'c_int(nConstraints)'
    if not (jacobianOption is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBIAN_OPTION)
        evalstring += ','
        evalstring += 'c_int(jacobianOption)'
    if not (yprimeMethod is None):
        evalstring += ','
        evalstring += repr(IMSL_YPRIME_METHOD)
        evalstring += ','
        evalstring += 'c_int(yprimeMethod)'
    if not (jacobianMatrixType is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBIAN_MATRIX_TYPE)
        evalstring += ','
        evalstring += 'c_int(jacobianMatrixType)'
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSL_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (nLowerDiag is None):
        evalstring += ','
        evalstring += repr(IMSL_N_LOWER_DIAG)
        evalstring += ','
        evalstring += 'c_int(nLowerDiag)'
    if not (nUpperDiag is None):
        evalstring += ','
        evalstring += repr(IMSL_N_UPPER_DIAG)
        evalstring += ','
        evalstring += 'c_int(nUpperDiag)'
    if not (relativeTolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_RELATIVE_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(relativeTolerance)'
    if not (absoluteTolerance is None):
        evalstring += ','
        evalstring += repr(IMSL_ABSOLUTE_TOLERANCE)
        evalstring += ','
        # evalstring +='c_double(absoluteTolerance)'
        absoluteTolerance = toNumpyArray(
            absoluteTolerance, 'absoluteTolerance', shape=shape, dtype='double', expectedShape=(neq))
        evalstring += 'absoluteTolerance.ctypes.data_as(c_void_p)'
    if not (initialStepsize is None):
        evalstring += ','
        evalstring += repr(IMSL_INITIAL_STEPSIZE)
        evalstring += ','
        evalstring += 'c_double(initialStepsize)'
    if not (maxStepsize is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_STEPSIZE)
        evalstring += ','
        evalstring += 'c_double(maxStepsize)'
    if not (maxOrder is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_ORDER)
        evalstring += ','
        evalstring += 'c_int(maxOrder)'
    if not (maxNumberSteps is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_NUMBER_STEPS)
        evalstring += ','
        evalstring += 'c_int(maxNumberSteps)'
    if not (integrationLimit is None):
        evalstring += ','
        evalstring += repr(IMSL_INTEGRATION_LIMIT)
        evalstring += ','
        evalstring += 'c_double(integrationLimit)'
    if not (orderMagnitudeEst is None):
        evalstring += ','
        evalstring += repr(IMSL_ORDER_MAGNITUDE_EST)
        evalstring += ','
        evalstring += 'c_double(orderMagnitudeEst)'
    """
    if not (gcnWData is None):
        evalstring +=','
        evalstring += repr(IMSL_GCN_W_DATA)
        checkForDict(gcnWData,'gcnWData',['gcnWData','t','y','yprime','delta','d','ires','data'])
        evalstring +=','
        tmp_gcnWData_gcnWData_param = gcnWData['gcnWData']
        checkForCallable(tmp_gcnWData_gcnWData_param,'gcnWData')
        TMP_GCNWDATA_GCNWDATA=CFUNCTYPE(None,c_int,c_double,POINTER(c_double),POINTER(c_double),POINTER(c_double),POINTER(c_double),c_int,POINTER(c_int),POINTER(c_double))
        tmp_gcnWData_gcnWData=TMP_GCNWDATA_GCNWDATA(tmp_gcnWData_gcnWData_param)
        evalstring += 'tmp_gcnWData_gcnWData'
        evalstring +=','
        evalstring +='c_int(gcnWData_neq_tmp)'
        evalstring +=','
        gcnWData_t_tmp = gcnWData['t']
        evalstring +='c_double(gcnWData_t_tmp)'
        evalstring +=','
        gcnWData_y_tmp = gcnWData['y']
        gcnWData_y_tmp = toNumpyArray(gcnWData_y_tmp, 'y', shape=shape, dtype='double', expectedShape=(0))
        evalstring +='gcnWData_y_tmp.ctypes.data_as(c_void_p)'
        gcnWData_neq_tmp=shape[0]
        evalstring +=','
        gcnWData_yprime_tmp = gcnWData['yprime']
        gcnWData_yprime_tmp = toNumpyArray(gcnWData_yprime_tmp, 'yprime', shape=shape, dtype='double', expectedShape=(gcnWData_neq_tmp))
        evalstring +='gcnWData_yprime_tmp.ctypes.data_as(c_void_p)'
        evalstring +=','
        gcnWData_delta_tmp = gcnWData['delta']
        gcnWData_delta_tmp = toNumpyArray(delta, 'delta', shape=shape, dtype='double', expectedShape=custom code max(gcnWData_neq_tmp,ncon))
        evalstring +='gcnWData_delta_tmp.ctypes.data_as(c_void_p)'
        evalstring +=','
        gcnWData_d_tmp = gcnWData['d']
        gcnWData_d_tmp = toNumpyArray(d, 'd', shape=shape, dtype='double', expectedShape=(0,gcnWData_neq_tmp))
        evalstring +='gcnWData_d_tmp.ctypes.data_as(c_void_p)'
        gcnWData_ldd_tmp=shape[0]
        evalstring +=','
        evalstring +='c_int(gcnWData_ldd_tmp)'
        evalstring +=','
        gcnWData_ires_tmp = gcnWData['ires']
        gcnWData_ires_tmp=ires[0]
        if (not(isinstance(gcnWData_ires_tmp, c_int))):
                gcnWData_ires_tmp=c_int(ires[0])
        evalstring +='byref(gcnWData_ires_tmp)'
        evalstring +=','
        gcnWData_data_tmp = gcnWData['data']
        gcnWData_data_tmp = toNumpyArray(gcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring +='gcnWData_data_tmp.ctypes.data_as(c_void_p)'
    """
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(t_tmp, inout=True, shape=(1), pyvar=t)
    processRet(ido_tmp, inout=True, shape=(1), pyvar=ido)
    # processRet(y_tmp, inout=True, shape=(gcnWData_neq_tmp), pyvar=y)
    # processRet(yprime_tmp, inout=True, shape=(gcnWData_neq_tmp), pyvar=yprime)
    processRet(y_tmp, inout=True, shape=(neq), pyvar=y)
    processRet(yprime_tmp, inout=True, shape=(neq), pyvar=yprime)
    """
    if not (gcnWData is None):
        processRet(gcnWData_delta_tmp, shape=(custom code max(gcnWData_neq_tmp,ncon)), key='delta', inout=True, pyvar=gcnWData)
        processRet(gcnWData_d_tmp, shape=(gcnWData_ldd_tmp,gcnWData_neq_tmp), key='d', inout=True, pyvar=gcnWData)
        processRet(gcnWData_ires_tmp, shape=(1), key='ires', inout=True, pyvar=gcnWData)
    """
    return
