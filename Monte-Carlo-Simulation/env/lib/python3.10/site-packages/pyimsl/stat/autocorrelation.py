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

IMSLS_PRINT_LEVEL = 20530
IMSLS_ACV = 30001
IMSLS_SEAC = 30003
IMSLS_X_MEAN_IN = 30005
IMSLS_X_MEAN_OUT = 30006
imslstat = loadimsl(STAT)


def autocorrelation(x, lagmax, printLevel=None, acv=None, seac=None, xMeanIn=None, xMeanOut=None):
    """ Computes the sample autocorrelation function of a stationary time series.
    """
    imslstat.imsls_d_autocorrelation.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_autocorrelation('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(lagmax)'
    if not (printLevel is None):
        evalstring += ','
        evalstring += repr(IMSLS_PRINT_LEVEL)
        evalstring += ','
        evalstring += 'c_int(printLevel)'
    if not (acv is None):
        evalstring += ','
        evalstring += repr(IMSLS_ACV)
        checkForList(acv, 'acv')
        evalstring += ','
        acv_acv_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(acv_acv_tmp)'
    if not (seac is None):
        evalstring += ','
        evalstring += repr(IMSLS_SEAC)
        checkForDict(seac, 'seac', ['seOption'])
        evalstring += ','
        seac_standardErrors_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(seac_standardErrors_tmp)'
        evalstring += ','
        seac_seOption_tmp = seac['seOption']
        evalstring += 'c_int(seac_seOption_tmp)'
    if not (xMeanIn is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_MEAN_IN)
        evalstring += ','
        evalstring += 'c_double(xMeanIn)'
    if not (xMeanOut is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_MEAN_OUT)
        checkForList(xMeanOut, 'xMeanOut')
        evalstring += ','
        xMeanOut_xMeanOut_tmp = c_double()
        evalstring += 'byref(xMeanOut_xMeanOut_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (acv is None):
        processRet(acv_acv_tmp, shape=(lagmax + 1), pyvar=acv)
    if not (seac is None):
        processRet(seac_standardErrors_tmp, shape=(
            lagmax), key='standardErrors', pyvar=seac)
    if not (xMeanOut is None):
        processRet(xMeanOut_xMeanOut_tmp, shape=1, pyvar=xMeanOut)
    return processRet(result, shape=(lagmax + 1), result=True)
