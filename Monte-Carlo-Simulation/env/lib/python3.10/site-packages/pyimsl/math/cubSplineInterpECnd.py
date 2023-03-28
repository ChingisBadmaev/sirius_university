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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, checkForDict, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import POINTER, c_double, c_int, c_void_p
from .mathStructs import Imsl_d_ppoly

IMSL_LEFT = 10031
IMSL_RIGHT = 10032
IMSL_PERIODIC = 10030
imslmath = loadimsl(MATH)


def cubSplineInterpECnd(xdata, fdata, left=None, right=None, periodic=None):
    """ Computes a cubic spline interpolant, specifying various endpoint conditions. The default interpolant satisfies the "not-a-knot" condition.
    """
    imslmath.imsl_d_cub_spline_interp_e_cnd.restype = POINTER(Imsl_d_ppoly)
    shape = []
    evalstring = 'imslmath.imsl_d_cub_spline_interp_e_cnd('
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
    if not (left is None):
        evalstring += ','
        evalstring += repr(IMSL_LEFT)
        checkForDict(left, 'left', ['ileft', 'left'])
        evalstring += ','
        left_ileft_tmp = left['ileft']
        evalstring += 'c_int(left_ileft_tmp)'
        evalstring += ','
        left_left_tmp = left['left']
        evalstring += 'c_double(left_left_tmp)'
    if not (right is None):
        evalstring += ','
        evalstring += repr(IMSL_RIGHT)
        checkForDict(right, 'right', ['iright', 'right'])
        evalstring += ','
        right_iright_tmp = right['iright']
        evalstring += 'c_int(right_iright_tmp)'
        evalstring += ','
        right_right_tmp = right['right']
        evalstring += 'c_double(right_right_tmp)'
    checkForBoolean(periodic, 'periodic')
    if (periodic):
        evalstring += ','
        evalstring += repr(IMSL_PERIODIC)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
