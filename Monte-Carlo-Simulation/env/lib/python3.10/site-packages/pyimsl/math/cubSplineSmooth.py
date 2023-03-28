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
from ctypes import POINTER, c_double, c_int, c_void_p
from .mathStructs import Imsl_d_ppoly

IMSL_WEIGHTS = 10141
IMSL_SMOOTHING_PAR = 10146
imslmath = loadimsl(MATH)


def cubSplineSmooth(xdata, fdata, weights=None, smoothingPar=None):
    """ Computes a smooth cubic spline approximation to noisy data by using cross-validation to estimate the smoothing parameter or by directly choosing the smoothing parameter.
    """
    imslmath.imsl_d_cub_spline_smooth.restype = POINTER(Imsl_d_ppoly)
    shape = []
    evalstring = 'imslmath.imsl_d_cub_spline_smooth('
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
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSL_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(ndata))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (smoothingPar is None):
        evalstring += ','
        evalstring += repr(IMSL_SMOOTHING_PAR)
        evalstring += ','
        evalstring += 'c_double(smoothingPar)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
