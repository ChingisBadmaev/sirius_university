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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, var
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_MAX_SIGMA = 30043
IMSLS_A = 30041
IMSLS_AIC = 30042
IMSLS_VAR = 30040
IMSLS_VAR_COL_DIM = 30038
imslstat = loadimsl(STAT)


def garch(p, q, y, xguess, maxSigma=None, a=None, aic=None, var=None, varColDim=None):
    """ Computes estimates of the parameters of a GARCH(p,q) model.
    """
    imslstat.imsls_d_garch.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_garch('
    evalstring += 'c_int(p)'
    evalstring += ','
    evalstring += 'c_int(q)'
    evalstring += ','
    evalstring += 'c_int(m)'
    evalstring += ','
    y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'y.ctypes.data_as(c_void_p)'
    m = shape[0]
    evalstring += ','
    xguess = toNumpyArray(xguess, 'xguess', shape=shape,
                          dtype='double', expectedShape=(p + q + 1))
    evalstring += 'xguess.ctypes.data_as(c_void_p)'
    if not (maxSigma is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_SIGMA)
        evalstring += ','
        evalstring += 'c_double(maxSigma)'
    if not (a is None):
        evalstring += ','
        evalstring += repr(IMSLS_A)
        checkForList(a, 'a')
        evalstring += ','
        a_a_tmp = c_double()
        evalstring += 'byref(a_a_tmp)'
    if not (aic is None):
        evalstring += ','
        evalstring += repr(IMSLS_AIC)
        checkForList(aic, 'aic')
        evalstring += ','
        aic_aic_tmp = c_double()
        evalstring += 'byref(aic_aic_tmp)'
    if not (var is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR)
        checkForList(var, 'var')
        evalstring += ','
        var_var_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(var_var_tmp)'
    if not (varColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_VAR_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(varColDim)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (a is None):
        processRet(a_a_tmp, shape=1, pyvar=a)
    if not (aic is None):
        processRet(aic_aic_tmp, shape=1, pyvar=aic)
    if not (var is None):
        processRet(var_var_tmp, shape=(p + q + 1, p + q + 1), pyvar=var)
    return processRet(result, shape=(p + q + 1), result=True)
