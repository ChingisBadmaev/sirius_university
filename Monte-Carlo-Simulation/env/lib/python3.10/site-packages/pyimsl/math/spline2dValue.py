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


def spline2dValue(x, y, sp, deriv=None, grid=None):
    """ Computes the value of a tensor-product spline or the value of one of its partial derivatives.
    """
    imslmath.imsl_d_spline_2d_value.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_spline_2d_value('
    evalstring += 'c_double(x)'
    evalstring += ','
    evalstring += 'c_double(y)'
    evalstring += ','
    evalstring += 'sp'
    if not (deriv is None):
        evalstring += ','
        evalstring += repr(IMSL_DERIV)
        checkForDict(deriv, 'deriv', ['x_partial', 'y_partial'])
        evalstring += ','
        deriv_xPartial_tmp = deriv['x_partial']
        evalstring += 'c_int(deriv_xPartial_tmp)'
        evalstring += ','
        deriv_yPartial_tmp = deriv['y_partial']
        evalstring += 'c_int(deriv_yPartial_tmp)'
    if not (grid is None):
        evalstring += ','
        evalstring += repr(IMSL_GRID)
        checkForDict(grid, 'grid', ['xvec', 'yvec', 'value'])
        evalstring += ','
        evalstring += 'c_int(grid_nx_tmp)'
        evalstring += ','
        grid_xvec_tmp = grid['xvec']
        grid_xvec_tmp = toNumpyArray(
            grid_xvec_tmp, 'xvec', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'grid_xvec_tmp.ctypes.data_as(c_void_p)'
        grid_nx_tmp = shape[0]
        evalstring += ','
        evalstring += 'c_int(grid_ny_tmp)'
        evalstring += ','
        grid_yvec_tmp = grid['yvec']
        grid_yvec_tmp = toNumpyArray(
            grid_yvec_tmp, 'yvec', shape=shape, dtype='double', expectedShape=(0))
        evalstring += 'grid_yvec_tmp.ctypes.data_as(c_void_p)'
        grid_ny_tmp = shape[0]
        evalstring += ','
        grid_value_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(grid_value_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if not (grid is None):
        processRet(grid_value_tmp, shape=(
            grid_nx_tmp, grid_ny_tmp), key='value', pyvar=grid)
    return result
