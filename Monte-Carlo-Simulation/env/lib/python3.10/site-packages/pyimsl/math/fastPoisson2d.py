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
from pyimsl.util.imslUtils import MATH, checkForCallable, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape, size
from ctypes import CFUNCTYPE, POINTER, c_double, c_int, c_void_p

IMSL_ORDER = 10036
IMSL_RHS_PDE_W_DATA = 13105
IMSL_RHS_BC_W_DATA = 13106

# Constants for rhsBc pdeSide (first argument):
RIGHT_SIDE = 0
BOTTOM_SIDE = 1
LEFT_SIDE = 2
TOP_SIDE = 3

# Constants for bcType
DIRICHLET_BC = 1
NEUMANN_BC = 2
PERIODIC_BC = 3

imslmath = loadimsl(MATH)


def fastPoisson2d(rhsPde, rhsBc, coeffU, nx, ny, ax, bx, ay, by, bcType, order=None, rhsPdeWData=None, rhsBcWData=None):
    """ Solves Poisson's or Helmholtz's equation on a two-dimensional rectangle using a fast Poisson solver based on the HODIE finite-difference scheme on a uniform mesh.
    """
    imslmath.imsl_d_fast_poisson_2d.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_fast_poisson_2d('
    checkForCallable(rhsPde, 'rhsPde')
    TMP_RHSPDE = CFUNCTYPE(c_double, c_double, c_double)
    tmp_rhsPde = TMP_RHSPDE(rhsPde)
    evalstring += 'tmp_rhsPde'
    evalstring += ','
    checkForCallable(rhsBc, 'rhsBc')
    TMP_RHSBC = CFUNCTYPE(c_double, c_int, c_double, c_double)
    tmp_rhsBc = TMP_RHSBC(rhsBc)
    evalstring += 'tmp_rhsBc'
    evalstring += ','
    evalstring += 'c_double(coeffU)'
    evalstring += ','
    evalstring += 'c_int(nx)'
    evalstring += ','
    evalstring += 'c_int(ny)'
    evalstring += ','
    evalstring += 'c_double(ax)'
    evalstring += ','
    evalstring += 'c_double(bx)'
    evalstring += ','
    evalstring += 'c_double(ay)'
    evalstring += ','
    evalstring += 'c_double(by)'
    evalstring += ','
    bcType = toNumpyArray(bcType, 'bcType', shape=shape,
                          dtype='int', expectedShape=(4))
    evalstring += 'bcType.ctypes.data_as(c_void_p)'
    if not (order is None):
        evalstring += ','
        evalstring += repr(IMSL_ORDER)
        evalstring += ','
        evalstring += 'c_int(order)'
    if not (rhsPdeWData is None):
        evalstring += ','
        evalstring += repr(IMSL_RHS_PDE_W_DATA)
        checkForList(rhsPdeWData, 'rhsPdeWData', size=2)
        evalstring += ','
        tmp_rhsPdeWData_rhsPdeWData_param = rhsPdeWData[0]
        checkForCallable(tmp_rhsPdeWData_rhsPdeWData_param, 'rhsPdeWData')
        TMP_RHSPDEWDATA_RHSPDEWDATA = CFUNCTYPE(
            c_double, c_double, c_double, POINTER(c_double))
        tmp_rhsPdeWData_rhsPdeWData = TMP_RHSPDEWDATA_RHSPDEWDATA(
            tmp_rhsPdeWData_rhsPdeWData_param)
        evalstring += 'tmp_rhsPdeWData_rhsPdeWData'
        evalstring += ','
        rhsPdeWData_data_tmp = rhsPdeWData[1]
        rhsPdeWData_data_tmp = toNumpyArray(
            rhsPdeWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'rhsPdeWData_data_tmp.ctypes.data_as(c_void_p)'
    if not (rhsBcWData is None):
        evalstring += ','
        evalstring += repr(IMSL_RHS_BC_W_DATA)
        checkForList(rhsBcWData, 'rhsBcWData', size=2)
        evalstring += ','
        tmp_rhsBcWData_rhsBcWData_param = rhsBcWData[0]
        checkForCallable(tmp_rhsBcWData_rhsBcWData_param, 'rhsBcWData')
        TMP_RHSBCWDATA_RHSBCWDATA = CFUNCTYPE(
            c_double, c_int, c_double, c_double, POINTER(c_double))
        tmp_rhsBcWData_rhsBcWData = TMP_RHSBCWDATA_RHSBCWDATA(
            tmp_rhsBcWData_rhsBcWData_param)
        evalstring += 'tmp_rhsBcWData_rhsBcWData'
        evalstring += ','
        rhsBcWData_data_tmp = rhsBcWData[1]
        rhsBcWData_data_tmp = toNumpyArray(
            rhsBcWData_data_tmp, 'data', shape=shape, dtype='double')
        evalstring += 'rhsBcWData_data_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(nx, ny), result=True)
