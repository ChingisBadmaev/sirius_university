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
from pyimsl.util.imslUtils import MATH, checkForList, checkForDict, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import POINTER, c_int, c_void_p
from .mathStructs import Imsl_d_spline

IMSL_ORDER = 10036
IMSL_KNOTS = 10035
IMSL_FDATA_COL_DIM = 10140
imslmath = loadimsl(MATH)


def spline2dInterp(xdata, ydata, fdata, order=None, knots=None, fdataColDim=None):
    """ Computes a two-dimensional, tensor-product spline interpolant from two-dimensional, tensor-product data.
    """
    imslmath.imsl_d_spline_2d_interp.restype = POINTER(Imsl_d_spline)
    shape = []
    evalstring = 'imslmath.imsl_d_spline_2d_interp('
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
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
