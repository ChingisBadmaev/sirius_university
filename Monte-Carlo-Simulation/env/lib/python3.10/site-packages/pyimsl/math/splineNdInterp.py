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
from numpy import *
from ctypes import *

IMSL_NDEGREE = 15034
IMSL_ORDER = 10036
IMSL_DERIV = 10028
IMSL_ERR_EST = 10020
imslstat = loadimsl(MATH)


def splineNdInterp(d, x, xdata, fdata, nDegree=None, order=None, deriv=None, errorEst=None):
    imslstat.imsl_d_spline_nd_interp.restype = c_double
    shape = []
    evalstring = 'imslstat.imsl_d_spline_nd_interp('
    evalstring += 'c_int(n)'
    evalstring += ','
    d_tmp = d[:]
    d = toNumpyArray(d, 'd', shape=shape, dtype='int', expectedShape=(0))
    evalstring += 'd.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(n))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    evalstring += ','
    xdata = toNumpyArray(xdata, 'xdata', shape=shape,
                         dtype='double', expectedShape=(n, max(d)))
    evalstring += 'xdata.ctypes.data_as(c_void_p)'
    evalstring += ','
    tmpsize = []
#    for z in range(len(d)):
#        tmpsize.append(d[z])
    fdata = toNumpyArray(fdata, 'fdata', shape=shape,
                         dtype='double', expectedShape=tuple(d_tmp))
    evalstring += 'fdata.ctypes.data_as(c_void_p)'
    if not (nDegree is None):
        evalstring += ','
        evalstring += repr(IMSL_NDEGREE)
        evalstring += ','
        nDegree = toNumpyArray(
            nDegree, 'nDegree', shape=shape, dtype='int', expectedShape=(n))
        evalstring += 'nDegree.ctypes.data_as(c_void_p)'
    if not (order is None):
        evalstring += ','
        evalstring += repr(IMSL_ORDER)
        evalstring += ','
        evalstring += 'c_int(order)'
        order_size = order
    else:
        order_size = 0
    if not (deriv is None):
        evalstring += ','
        evalstring += repr(IMSL_DERIV)
        checkForList(deriv, 'deriv')
        evalstring += ','
        deriv_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(deriv_tmp)'
    if not (errorEst is None):
        evalstring += ','
        evalstring += repr(IMSL_ERR_EST)
        checkForList(errorEst, 'errorEst')
        evalstring += ','
        errorEst_error_tmp = c_double()
        evalstring += 'byref(errorEst_error_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (deriv is None):
        tmp = (order_size + 1,) * n
        processRet(deriv_tmp, shape=tmp, pyvar=deriv)
    if not (errorEst is None):
        processRet(errorEst_error_tmp, shape=(1), pyvar=errorEst)
    return result
