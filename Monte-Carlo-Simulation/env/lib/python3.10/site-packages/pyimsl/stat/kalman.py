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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_UPDATE = 25920
IMSLS_Z_COL_DIM = 40010
IMSLS_R_COL_DIM = 16072
IMSLS_T = 40015
IMSLS_T_COL_DIM = 40011
IMSLS_Q = 14000
IMSLS_Q_COL_DIM = 14040
IMSLS_TOLERANCE = 15040
IMSLS_V = 15290
IMSLS_COVV = 40014
imslstat = loadimsl(STAT)


def kalman(b, covb, n, ss, alndet, update=None, zColDim=None, rColDim=None, t=None, tColDim=None, q=None, qColDim=None, tolerance=None, v=None, covv=None):
    """ Performs Kalman filtering and evaluates the likelihood function for the state-space model.
    """
    imslstat.imsls_d_kalman.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_kalman('
    evalstring += 'c_int(nb)'
    evalstring += ','
    b_tmp = toNumpyArray(b, 'b', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'b_tmp.ctypes.data_as(c_void_p)'
    nb = shape[0]
    evalstring += ','
    covb_tmp = toNumpyArray(covb, 'covb', shape=shape,
                            dtype='double', expectedShape=(nb, nb))
    evalstring += 'covb_tmp.ctypes.data_as(c_void_p)'
    evalstring += ','

    checkForList(n, 'n', size=1)
    n_tmp = c_int(n[0])
    evalstring += 'byref(n_tmp)'
    evalstring += ','

    checkForList(ss, 'ss', size=1)
    ss_tmp = c_double(ss[0])
    evalstring += 'byref(ss_tmp)'
    evalstring += ','

    checkForList(alndet, 'alndet', size=1)
    alndet_tmp = c_double(alndet[0])
    evalstring += 'byref(alndet_tmp)'

    if not (update is None):
        evalstring += ','
        evalstring += repr(IMSLS_UPDATE)
        checkForDict(update, 'update', ['y', 'z', 'r'])
        evalstring += ','
        evalstring += 'c_int(update_ny_tmp)'
        evalstring += ','
        update_y_tmp = update['y']
        update_y_tmp = toNumpyArray(
            update_y_tmp, 'y', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'update_y_tmp.ctypes.data_as(c_void_p)'
        update_ny_tmp = shape[0]
        evalstring += ','
        update_z_tmp = update['z']
        update_z_tmp = toNumpyArray(
            update_z_tmp, 'z', shape=shape, dtype='double', expectedShape=(update_ny_tmp, nb))
        evalstring += 'update_z_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        update_r_tmp = update['r']
        update_r_tmp = toNumpyArray(update_r_tmp, 'r', shape=shape,
                                    dtype='double', expectedShape=(update_ny_tmp, update_ny_tmp))
        evalstring += 'update_r_tmp.ctypes.data_as(c_void_p)'
    if not (zColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_Z_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(zColDim)'
    if not (rColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_R_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(rColDim)'
    if not (t is None):
        evalstring += ','
        evalstring += repr(IMSLS_T)
        evalstring += ','
        t = toNumpyArray(t, 't', shape=shape, dtype='double',
                         expectedShape=(0, nb))
        evalstring += 't.ctypes.data_as(c_void_p)'
    if not (tColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_T_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(tColDim)'
    if not (q is None):
        evalstring += ','
        evalstring += repr(IMSLS_Q)
        evalstring += ','
        q = toNumpyArray(q, 'q', shape=shape, dtype='double',
                         expectedShape=(0, nb))
        evalstring += 'q.ctypes.data_as(c_void_p)'
    if not (qColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_Q_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(qColDim)'
    if not (tolerance is None):
        evalstring += ','
        evalstring += repr(IMSLS_TOLERANCE)
        evalstring += ','
        evalstring += 'c_double(tolerance)'
    if not (v is None):
        evalstring += ','
        evalstring += repr(IMSLS_V)
        checkForList(v, 'v')
        evalstring += ','
        v_v_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(v_v_tmp)'
    if not (covv is None):
        evalstring += ','
        evalstring += repr(IMSLS_COVV)
        checkForList(covv, 'covv')
        evalstring += ','
        covv_covv_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(covv_covv_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(b_tmp, inout=True, shape=(nb), pyvar=b)
    processRet(covb_tmp, inout=True, shape=(nb, nb), pyvar=covb)
    processRet(n_tmp, inout=True, shape=1, pyvar=n)
    processRet(ss_tmp, inout=True, shape=1, pyvar=ss)
    processRet(alndet_tmp, inout=True, shape=1, pyvar=alndet)
    if not (v is None):
        processRet(v_v_tmp, shape=(update_ny_tmp), pyvar=v)
    if not (covv is None):
        processRet(covv_covv_tmp, shape=(
            update_ny_tmp, update_ny_tmp), pyvar=covv)
    return
