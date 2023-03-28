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
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .statStructs import Imsls_d_regression

IMSLS_G = 20943
IMSLS_U = 15180
imslstat = loadimsl(STAT)


def hypothesisScph(regressionInfo, h, dfh, g=None, u=None):
    """ Computes the matrix of sums of squares and crossproducts for a multivariate general linear hypothesis given the regression fit.
    """
    imslstat.imsls_d_hypothesis_scph.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_hypothesis_scph('
    evalstring += 'regressionInfo'
    evalstring += ','
    evalstring += 'c_int(nh)'
    evalstring += ','
    h = toNumpyArray(h, 'h', shape=shape, dtype='double', expectedShape=(0, 0))
    evalstring += 'h.ctypes.data_as(c_void_p)'
    nh = shape[0]
    evalstring += ','
    dfh_tmp = c_double()
    evalstring += 'byref(dfh_tmp)'
    if not (g is None):
        evalstring += ','
        evalstring += repr(IMSLS_G)
        checkForList(g, 'g')
        evalstring += ','
        g_g_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(g_g_tmp)'
    if not (u is None):
        evalstring += ','
        evalstring += repr(IMSLS_U)
        checkForList(u, 'u', size=1)
        evalstring += ','
        evalstring += 'c_int(u_nu_tmp)'
        evalstring += ','
        u_u_tmp = toNumpyArray(u, 'u', shape=shape,
                               dtype='double', expectedShape=(nDependent, 0))
        evalstring += 'u_u_tmp.ctypes.data_as(c_void_p)'
        u_nu_tmp = shape[1]
    else:
        u_nu_tmp = regressionInfo[0].n_dependent
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(dfh_tmp, pyvar=dfh)
    if not (g is None):
        processRet(g_g_tmp, shape=(nh, u_nu_tmp), pyvar=g)
    return processRet(result, shape=(u_nu_tmp, u_nu_tmp), result=True)
