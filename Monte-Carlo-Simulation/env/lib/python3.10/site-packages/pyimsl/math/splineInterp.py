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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_int, c_void_p
from .mathStructs import Imsl_d_spline

IMSL_ORDER = 10036
IMSL_KNOTS = 10035
imslmath = loadimsl(MATH)


def splineInterp(xdata, fdata, order=None, knots=None):
    """ Compute a spline interpolant.
    """
    imslmath.imsl_d_spline_interp.restype = POINTER(Imsl_d_spline)
    shape = []
    evalstring = 'imslmath.imsl_d_spline_interp('
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
                             dtype='double', expectedShape=(ndata + order))
        evalstring += 'knots.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
