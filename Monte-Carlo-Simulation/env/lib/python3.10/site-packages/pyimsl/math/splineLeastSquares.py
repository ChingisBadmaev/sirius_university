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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, toNumpyArray, processRet
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .mathStructs import Imsl_d_spline

IMSL_SSE = 10145
IMSL_WEIGHTS = 10141
IMSL_ORDER = 10036
IMSL_KNOTS = 10035
IMSL_OPTIMIZE = 10143
imslmath = loadimsl(MATH)


def splineLeastSquares(xdata, fdata, splineSpaceDim, sse=None, weights=None, order=None, knots=None, optimize=None):
    """ Computes a least-squares spline approximation.
    """
    imslmath.imsl_d_spline_least_squares.restype = POINTER(Imsl_d_spline)
    shape = []
    evalstring = 'imslmath.imsl_d_spline_least_squares('
    evalstring += 'c_int(ndata)'
    evalstring += ','
    xdata = toNumpyArray(xdata, 'xdata', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'xdata.ctypes.data_as(c_void_p)'
    ndata = shape[0]
    evalstring += ','
    fdata = toNumpyArray(fdata, 'fdata', shape=shape,
                         dtype='double', expectedShape=(ndata))
    evalstring += 'fdata.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(splineSpaceDim)'
    if not (sse is None):
        evalstring += ','
        evalstring += repr(IMSL_SSE)
        checkForList(sse, 'sse')
        evalstring += ','
        sse_sseErr_tmp = c_double()
        evalstring += 'byref(sse_sseErr_tmp)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSL_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(ndata))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (order is None):
        evalstring += ','
        evalstring += repr(IMSL_ORDER)
        evalstring += ','
        evalstring += 'c_int(order)'
    else:
        order = 4
    if not (knots is None):
        evalstring += ','
        evalstring += repr(IMSL_KNOTS)
        evalstring += ','
        knots = toNumpyArray(knots, 'knots', shape=shape,
                             dtype='double', expectedShape=(splineSpaceDim + order))
        evalstring += 'knots.ctypes.data_as(c_void_p)'
    checkForBoolean(optimize, 'optimize')
    if (optimize):
        evalstring += ','
        evalstring += repr(IMSL_OPTIMIZE)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (sse is None):
        processRet(sse_sseErr_tmp, shape=1, pyvar=sse)
    return result
