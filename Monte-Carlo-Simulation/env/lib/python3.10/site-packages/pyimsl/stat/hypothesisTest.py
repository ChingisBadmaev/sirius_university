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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, checkForDict, processRet
from numpy import double, dtype, shape, size
from ctypes import byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_regression

IMSLS_U = 15180
IMSLS_WILK_LAMBDA = 20950
IMSLS_ROY_MAX_ROOT = 20951
IMSLS_HOTELLING_TRACE = 20952
IMSLS_PILLAI_TRACE = 20953
imslstat = loadimsl(STAT)


def hypothesisTest(regressionInfo, dfh, scph, u=None, wilkLambda=None, royMaxRoot=None, hotellingTrace=None, pillaiTrace=None):
    """ Performs tests for a multivariate general linear hypothesis given the hypothesis sums of squares and crossproducts matrix.
    """
    imslstat.imsls_d_hypothesis_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_hypothesis_test('
    evalstring += 'regressionInfo'
    evalstring += ','
    evalstring += 'c_double(dfh)'
    evalstring += ','
    scph = toNumpyArray(scph, 'scph', shape=shape,
                        dtype='double', expectedShape=(0, 0))
    evalstring += 'scph.ctypes.data_as(c_void_p)'
    if not (u is None):
        evalstring += ','
        evalstring += repr(IMSLS_U)
        evalstring += ','
        evalstring += 'c_int(u_nu_tmp)'
        evalstring += ','
        nDependent = regressionInfo[0].n_dependent
        u_u_tmp = toNumpyArray(u, 'u', shape=shape,
                               dtype='double', expectedShape=(nDependent, 0))
        evalstring += 'u_u_tmp.ctypes.data_as(c_void_p)'
        u_nu_tmp = shape[1]
    if not (wilkLambda is None):
        evalstring += ','
        evalstring += repr(IMSLS_WILK_LAMBDA)
        checkForDict(wilkLambda, 'wilkLambda', [])
        evalstring += ','
        wilkLambda_value_tmp = c_double()
        evalstring += 'byref(wilkLambda_value_tmp)'
        evalstring += ','
        wilkLambda_pValue_tmp = c_double()
        evalstring += 'byref(wilkLambda_pValue_tmp)'
    if not (royMaxRoot is None):
        evalstring += ','
        evalstring += repr(IMSLS_ROY_MAX_ROOT)
        checkForDict(royMaxRoot, 'royMaxRoot', [])
        evalstring += ','
        royMaxRoot_value_tmp = c_double()
        evalstring += 'byref(royMaxRoot_value_tmp)'
        evalstring += ','
        royMaxRoot_pValue_tmp = c_double()
        evalstring += 'byref(royMaxRoot_pValue_tmp)'
    if not (hotellingTrace is None):
        evalstring += ','
        evalstring += repr(IMSLS_HOTELLING_TRACE)
        checkForDict(hotellingTrace, 'hotellingTrace', [])
        evalstring += ','
        hotellingTrace_value_tmp = c_double()
        evalstring += 'byref(hotellingTrace_value_tmp)'
        evalstring += ','
        hotellingTrace_pValue_tmp = c_double()
        evalstring += 'byref(hotellingTrace_pValue_tmp)'
    if not (pillaiTrace is None):
        evalstring += ','
        evalstring += repr(IMSLS_PILLAI_TRACE)
        checkForDict(pillaiTrace, 'pillaiTrace', [])
        evalstring += ','
        pillaiTrace_value_tmp = c_double()
        evalstring += 'byref(pillaiTrace_value_tmp)'
        evalstring += ','
        pillaiTrace_pValue_tmp = c_double()
        evalstring += 'byref(pillaiTrace_pValue_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (wilkLambda is None):
        processRet(wilkLambda_value_tmp, shape=(
            1), key='value', pyvar=wilkLambda)
        processRet(wilkLambda_pValue_tmp, shape=(
            1), key='pValue', pyvar=wilkLambda)
    if not (royMaxRoot is None):
        processRet(royMaxRoot_value_tmp, shape=(
            1), key='value', pyvar=royMaxRoot)
        processRet(royMaxRoot_pValue_tmp, shape=(
            1), key='pValue', pyvar=royMaxRoot)
    if not (hotellingTrace is None):
        processRet(hotellingTrace_value_tmp, shape=(
            1), key='value', pyvar=hotellingTrace)
        processRet(hotellingTrace_pValue_tmp, shape=(
            1), key='pValue', pyvar=hotellingTrace)
    if not (pillaiTrace is None):
        processRet(pillaiTrace_value_tmp, shape=(
            1), key='value', pyvar=pillaiTrace)
        processRet(pillaiTrace_pValue_tmp, shape=(
            1), key='pValue', pyvar=pillaiTrace)
    return result
