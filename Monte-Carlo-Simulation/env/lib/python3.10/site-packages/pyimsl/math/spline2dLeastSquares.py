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
from pyimsl.util.imslUtils import MATH, checkForList, checkForDict, fatalErrorCheck, loadimsl, toNumpyArray, processRet
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .mathStructs import Imsl_d_spline

IMSL_SSE = 10145
IMSL_ORDER = 10036
IMSL_KNOTS = 10035
IMSL_FDATA_COL_DIM = 10140
IMSL_WEIGHTS = 10141
imslmath = loadimsl(MATH)


def spline2dLeastSquares(xdata, ydata, fdata, xSplineSpaceDim, ySplineSpaceDim, sse=None, order=None, knots=None, fdataColDim=None, weights=None):
    """ Computes a two-dimensional, tensor-product spline approximant using least squares.
    """
    imslmath.imsl_d_spline_2d_least_squares.restype = POINTER(Imsl_d_spline)
    shape = []
    evalstring = 'imslmath.imsl_d_spline_2d_least_squares('
    evalstring += 'c_int(numXdata)'
    evalstring += ','
    xdata = toNumpyArray(xdata, 'xdata', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'xdata.ctypes.data_as(c_void_p)'
    numXdata = shape[0]
    evalstring += ','
    evalstring += 'c_int(numYdata)'
    evalstring += ','
    ydata = toNumpyArray(ydata, 'ydata', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'ydata.ctypes.data_as(c_void_p)'
    numYdata = shape[0]
    evalstring += ','
    fdata = toNumpyArray(fdata, 'fdata', shape=shape,
                         dtype='double', expectedShape=(numXdata, numYdata))
    evalstring += 'fdata.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(xSplineSpaceDim)'
    evalstring += ','
    evalstring += 'c_int(ySplineSpaceDim)'
    if not (sse is None):
        evalstring += ','
        evalstring += repr(IMSL_SSE)
        checkForList(sse, 'sse')
        evalstring += ','
        sse_sse_tmp = c_double()
        evalstring += 'byref(sse_sse_tmp)'
    if not (order is None):
        evalstring += ','
        evalstring += repr(IMSL_ORDER)
        checkForDict(order, 'order', ['xorder', 'yorder'])
        evalstring += ','
        order_xorder_tmp = order['xorder']
        evalstring += 'c_int(order_xorder_tmp)'
        evalstring += ','
        order_yorder_tmp = order['yorder']
        evalstring += 'c_int(order_yorder_tmp)'
    if not (knots is None):
        evalstring += ','
        evalstring += repr(IMSL_KNOTS)
        checkForDict(knots, 'knots', ['xknots', 'yknots'])
        evalstring += ','
        knots_xknots_tmp = knots['xknots']
        knots_xknots_tmp = toNumpyArray(
            knots_xknots_tmp, 'xknots', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'knots_xknots_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        knots_yknots_tmp = knots['yknots']
        knots_yknots_tmp = toNumpyArray(
            knots_yknots_tmp, 'yknots', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'knots_yknots_tmp.ctypes.data_as(c_void_p)'
    if not (fdataColDim is None):
        evalstring += ','
        evalstring += repr(IMSL_FDATA_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(fdataColDim)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSL_WEIGHTS)
        checkForDict(weights, 'weights', ['xweights', 'yweights'])
        evalstring += ','
        weights_xweights_tmp = weights['xweights']
        weights_xweights_tmp = toNumpyArray(
            weights_xweights_tmp, 'xweights', shape=shape, dtype='double', expectedShape=(numXdata))
        evalstring += 'weights_xweights_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        weights_yweights_tmp = weights['yweights']
        weights_yweights_tmp = toNumpyArray(
            weights_yweights_tmp, 'yweights', shape=shape, dtype='double', expectedShape=(numYdata))
        evalstring += 'weights_yweights_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (sse is None):
        processRet(sse_sse_tmp, shape=1, pyvar=sse)
    return result
