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
from numpy import array, empty
from ctypes import *
from .mathStructs import Imsl_d_ppoly
from pyimsl.util.VersionFacade import VersionFacade

IMSL_TENSION = 15016
IMSL_CONTINUITY = 15017
IMSL_BIAS = 15018
IMSL_LEFT = 10031
IMSL_RIGHT = 10032
imslmath = loadimsl(MATH)


def cubSplineTcb(xdata, fdata, tension=None, continuity=None, bias=None, left=None, right=None):
    VersionFacade.checkVersion(7)
    imslmath.imsl_d_cub_spline_tcb.restype = POINTER(Imsl_d_ppoly)
    shape = []
    evalstring = 'imslmath.imsl_d_cub_spline_tcb('
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
    if not (tension is None):
        evalstring += ','
        evalstring += repr(IMSL_TENSION)
        evalstring += ','
        tension = toNumpyArray(
            tension, 'tension', shape=shape, dtype='double', expectedShape=(ndata))
        evalstring += 'tension.ctypes.data_as(c_void_p)'
    if not (continuity is None):
        evalstring += ','
        evalstring += repr(IMSL_CONTINUITY)
        evalstring += ','
        continuity = toNumpyArray(
            continuity, 'continuity', shape=shape, dtype='double', expectedShape=(ndata))
        evalstring += 'continuity.ctypes.data_as(c_void_p)'
    if not (bias is None):
        evalstring += ','
        evalstring += repr(IMSL_BIAS)
        evalstring += ','
        bias = toNumpyArray(bias, 'bias', shape=shape,
                            dtype='double', expectedShape=(ndata))
        evalstring += 'bias.ctypes.data_as(c_void_p)'
    if not (left is None):
        evalstring += ','
        evalstring += repr(IMSL_LEFT)
        evalstring += ','
        evalstring += 'c_double(left)'
    if not (right is None):
        evalstring += ','
        evalstring += repr(IMSL_RIGHT)
        evalstring += ','
        evalstring += 'c_double(right)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
