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

IMSL_FCN_W_DATA = 13101
IMSL_GCN_W_DATA = 13100
IMSL_HCN_W_DATA = 13109
IMSL_PCN_W_DATA = 13114
IMSL_QCN_W_DATA = 13115
IMSL_ERR_ABS = 10010
IMSL_ERR_FRAC = 15049
IMSL_ERR_REL = 10011
IMSL_ERR_PRIOR = 15051
IMSL_MAX_EVALS = 10277
IMSL_SINGULARITY = 15052
IMSL_N_EVALS = 10023
IMSL_ERR_EST = 10020
IMSL_ISTATUS = 15053
imslmath = loadimsl(MATH)


def intFcnSing3d(fcn, a, b, gcn, hcn, pcn, qcn, errAbs=None, errFrac=None, errRel=None, errPrior=None, maxEvals=None, singularity=None, nEvals=None, errEst=None, istatus=None):
    """ Integrates a function of three variables with a possible internal or endpoint singularity.
    """
    imslmath.imsl_d_int_fcn_sing_3d.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_int_fcn_sing_3d('
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_double, c_double, c_double, c_double)
    tmp_fcn = TMP_FCN(fcn)
    evalstring += 'tmp_fcn'
    evalstring += ','
    evalstring += 'c_double(a)'
    evalstring += ','
    evalstring += 'c_double(b)'
    evalstring += ','
    checkForCallable(gcn, 'gcn')
    TMP_GCN = CFUNCTYPE(c_double, c_double)
    tmp_gcn = TMP_GCN(gcn)
    evalstring += 'tmp_gcn'
    evalstring += ','
    checkForCallable(hcn, 'hcn')
    TMP_HCN = CFUNCTYPE(c_double, c_double)
    tmp_hcn = TMP_HCN(hcn)
    evalstring += 'tmp_hcn'
    evalstring += ','
    checkForCallable(pcn, 'pcn')
    TMP_PCN = CFUNCTYPE(c_double, c_double, c_double)
    tmp_pcn = TMP_PCN(pcn)
    evalstring += 'tmp_pcn'
    evalstring += ','
    checkForCallable(qcn, 'qcn')
    TMP_QCN = CFUNCTYPE(c_double, c_double, c_double)
    tmp_qcn = TMP_QCN(qcn)
    evalstring += 'tmp_qcn'
    """
    if not (fcnWData is None):
        evalstring +=','
        evalstring += repr(IMSL_FCN_W_DATA)
        checkForDict(fcnWData,'fcnWData',['fcnWData','x','y','z','errPost','data'])
        evalstring +=','
        tmp_fcnWData_fcnWData_param = fcnWData['fcnWData']
        checkForCallable(tmp_fcnWData_fcnWData_param,'fcnWData')
        TMP_FCNWDATA_FCNWDATA=CFUNCTYPE(c_double,c_double,c_double,c_double,POINTER(c_double),POINTER(c_double))
        tmp_fcnWData_fcnWData=TMP_FCNWDATA_FCNWDATA(tmp_fcnWData_fcnWData_param)
        evalstring += 'tmp_fcnWData_fcnWData'
        evalstring +=','
        fcnWData_x_tmp = fcnWData['x']
        evalstring +='c_double(fcnWData_x_tmp)'
        evalstring +=','
        fcnWData_y_tmp = fcnWData['y']
        evalstring +='c_double(fcnWData_y_tmp)'
        evalstring +=','
        fcnWData_z_tmp = fcnWData['z']
        evalstring +='c_double(fcnWData_z_tmp)'
        evalstring +=','
        fcnWData_errPost_tmp = fcnWData['errPost']
        fcnWData_errPost_tmp=errPost[0]
        if (not(isinstance(fcnWData_errPost_tmp, c_double))):
                fcnWData_errPost_tmp=c_double(errPost[0])
        evalstring +='byref(fcnWData_errPost_tmp)'
        evalstring +=','
        fcnWData_data_tmp = fcnWData['data']
        fcnWData_data_tmp = toNumpyArray(fcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring +='fcnWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (gcnWData is None):
        evalstring +=','
        evalstring += repr(IMSL_GCN_W_DATA)
        checkForDict(gcnWData,'gcnWData',['gcnWData','x','data'])
        evalstring +=','
        tmp_gcnWData_gcnWData_param = gcnWData['gcnWData']
        checkForCallable(tmp_gcnWData_gcnWData_param,'gcnWData')
        TMP_GCNWDATA_GCNWDATA=CFUNCTYPE(c_double,c_double,POINTER(c_double))
        tmp_gcnWData_gcnWData=TMP_GCNWDATA_GCNWDATA(tmp_gcnWData_gcnWData_param)
        evalstring += 'tmp_gcnWData_gcnWData'
        evalstring +=','
        gcnWData_x_tmp = gcnWData['x']
        evalstring +='c_double(gcnWData_x_tmp)'
        evalstring +=','
        gcnWData_data_tmp = gcnWData['data']
        gcnWData_data_tmp = toNumpyArray(gcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring +='gcnWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (hcnWData is None):
        evalstring +=','
        evalstring += repr(IMSL_HCN_W_DATA)
        checkForDict(hcnWData,'hcnWData',['hcnWData','x','data'])
        evalstring +=','
        tmp_hcnWData_hcnWData_param = hcnWData['hcnWData']
        checkForCallable(tmp_hcnWData_hcnWData_param,'hcnWData')
        TMP_HCNWDATA_HCNWDATA=CFUNCTYPE(c_double,c_double,POINTER(c_double))
        tmp_hcnWData_hcnWData=TMP_HCNWDATA_HCNWDATA(tmp_hcnWData_hcnWData_param)
        evalstring += 'tmp_hcnWData_hcnWData'
        evalstring +=','
        hcnWData_x_tmp = hcnWData['x']
        evalstring +='c_double(hcnWData_x_tmp)'
        evalstring +=','
        hcnWData_data_tmp = hcnWData['data']
        hcnWData_data_tmp = toNumpyArray(hcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring +='hcnWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (pcnWData is None):
        evalstring +=','
        evalstring += repr(IMSL_PCN_W_DATA)
        checkForDict(pcnWData,'pcnWData',['pcnWData','x','y','data'])
        evalstring +=','
        tmp_pcnWData_pcnWData_param = pcnWData['pcnWData']
        checkForCallable(tmp_pcnWData_pcnWData_param,'pcnWData')
        TMP_PCNWDATA_PCNWDATA=CFUNCTYPE(c_double,c_double,c_double,POINTER(c_double))
        tmp_pcnWData_pcnWData=TMP_PCNWDATA_PCNWDATA(tmp_pcnWData_pcnWData_param)
        evalstring += 'tmp_pcnWData_pcnWData'
        evalstring +=','
        pcnWData_x_tmp = pcnWData['x']
        evalstring +='c_double(pcnWData_x_tmp)'
        evalstring +=','
        pcnWData_y_tmp = pcnWData['y']
        evalstring +='c_double(pcnWData_y_tmp)'
        evalstring +=','
        pcnWData_data_tmp = pcnWData['data']
        pcnWData_data_tmp = toNumpyArray(pcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring +='pcnWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (qcnWData is None):
        evalstring +=','
        evalstring += repr(IMSL_QCN_W_DATA)
        checkForDict(qcnWData,'qcnWData',['qcnWData','x','y','data'])
        evalstring +=','
        tmp_qcnWData_qcnWData_param = qcnWData['qcnWData']
        checkForCallable(tmp_qcnWData_qcnWData_param,'qcnWData')
        TMP_QCNWDATA_QCNWDATA=CFUNCTYPE(c_double,c_double,c_double,POINTER(c_double))
        tmp_qcnWData_qcnWData=TMP_QCNWDATA_QCNWDATA(tmp_qcnWData_qcnWData_param)
        evalstring += 'tmp_qcnWData_qcnWData'
        evalstring +=','
        qcnWData_x_tmp = qcnWData['x']
        evalstring +='c_double(qcnWData_x_tmp)'
        evalstring +=','
        qcnWData_y_tmp = qcnWData['y']
        evalstring +='c_double(qcnWData_y_tmp)'
        evalstring +=','
        qcnWData_data_tmp = qcnWData['data']
        qcnWData_data_tmp = toNumpyArray(qcnWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring +='qcnWData_data_tmp.ctypes.data_as(c_void_p)'
    """
    if not (errAbs is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_ABS)
        evalstring += ','
        evalstring += 'c_double(errAbs)'
    if not (errFrac is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_FRAC)
        evalstring += ','
        evalstring += 'c_double(errFrac)'
    if not (errRel is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_REL)
        evalstring += ','
        evalstring += 'c_double(errRel)'
    if not (errPrior is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_PRIOR)
        evalstring += ','
        evalstring += 'c_double(errPrior)'
    if not (maxEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_MAX_EVALS)
        evalstring += ','
        evalstring += 'c_double(maxEvals)'
    if not (singularity is None):
        evalstring += ','
        evalstring += repr(IMSL_SINGULARITY)
        checkForDict(singularity, 'singularity', [
                     'singularity', 'singularityType'])
        evalstring += ','
        singularity_singularity_tmp = singularity['singularity']
        evalstring += 'c_double(singularity_singularity_tmp)'
        evalstring += ','
        singularity_singularityType_tmp = singularity['singularityType']
        evalstring += 'c_int(singularity_singularityType_tmp)'
    if not (nEvals is None):
        evalstring += ','
        evalstring += repr(IMSL_N_EVALS)
        checkForList(nEvals, 'nEvals')
        evalstring += ','
        nEvals_nEvals_tmp = c_int()
        evalstring += 'byref(nEvals_nEvals_tmp)'
    if not (errEst is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_EST)
        checkForList(errEst, 'errEst')
        evalstring += ','
        errEst_errEst_tmp = c_double()
        evalstring += 'byref(errEst_errEst_tmp)'
    if not (istatus is None):
        evalstring += ','
        evalstring += repr(IMSL_ISTATUS)
        checkForList(istatus, 'istatus')
        evalstring += ','
        istatus_istatus_tmp = c_int()
        evalstring += 'byref(istatus_istatus_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    # if not (fcnWData is None):
    #    processRet(fcnWData_errPost_tmp, shape=(1), key='errPost', inout=True, pyvar=fcnWData)
    if not (nEvals is None):
        processRet(nEvals_nEvals_tmp, shape=(1), pyvar=nEvals)
    if not (errEst is None):
        processRet(errEst_errEst_tmp, shape=(1), pyvar=errEst)
    if not (istatus is None):
        processRet(istatus_istatus_tmp, shape=(1), pyvar=istatus)
    return result
