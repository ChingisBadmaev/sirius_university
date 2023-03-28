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
from pyimsl.util.imslUtils import MATH, checkForBoolean, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_int, c_void_p
from .mathStructs import Imsl_d_ppoly

IMSL_CONCAVE = 10029
IMSL_CONCAVE_ITMAX = 10149
imslmath = loadimsl(MATH)


def cubSplineInterpShape(xdata, fdata, concave=None, concaveItmax=None):
    """ Computes a shape-preserving cubic spline.
    """
    imslmath.imsl_d_cub_spline_interp_shape.restype = POINTER(Imsl_d_ppoly)
    shape = []
    evalstring = 'imslmath.imsl_d_cub_spline_interp_shape('
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
    checkForBoolean(concave, 'concave')
    if (concave):
        evalstring += ','
        evalstring += repr(IMSL_CONCAVE)
    if not (concaveItmax is None):
        evalstring += ','
        evalstring += repr(IMSL_CONCAVE_ITMAX)
        evalstring += ','
        evalstring += 'c_int(concaveItmax)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
