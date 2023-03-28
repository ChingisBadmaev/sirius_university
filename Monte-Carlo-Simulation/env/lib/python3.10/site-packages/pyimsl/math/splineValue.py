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
from pyimsl.util.imslUtils import MATH, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p
from .mathStructs import Imsl_d_spline

IMSL_DERIV = 10028
IMSL_GRID = 11050
imslmath = loadimsl(MATH)


def splineValue(x, sp, deriv=None, grid=None):
    """ Computes the value of a spline or the value of one of its derivatives.
    """
    imslmath.imsl_d_spline_value.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_spline_value('
    evalstring += 'c_double(x)'
    evalstring += ','
    evalstring += 'sp'
    if not (deriv is None):
        evalstring += ','
        evalstring += repr(IMSL_DERIV)
        evalstring += ','
        evalstring += 'c_int(deriv)'
    if not (grid is None):
        evalstring += ','
        evalstring += repr(IMSL_GRID)
        checkForDict(grid, 'grid', ['xvec', 'value'])
        evalstring += ','
        evalstring += 'c_int(grid_n_tmp)'
        evalstring += ','
        grid_xvec_tmp = grid['xvec']
        grid_xvec_tmp = toNumpyArray(
            grid_xvec_tmp, 'xvec', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'grid_xvec_tmp.ctypes.data_as(c_void_p)'
        grid_n_tmp = shape[0]
        evalstring += ','
        grid_value_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(grid_value_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (grid is None):
        processRet(grid_value_tmp, shape=(grid_n_tmp), key='value', pyvar=grid)
    return result
