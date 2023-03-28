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
from pyimsl.util.imslUtils import MATH, checkForCallable, fatalErrorCheck, loadimsl, toNumpyArray, processRet
from numpy import double, dtype, ndarray, shape
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p, c_float
from pyimsl.util.CnlState import CnlState
from pyimsl.util.Translator import Translator
from pyimsl.util.imslUtils import isLinux64
imslmath = loadimsl(MATH)


def pdeMethodOfLines(t, tend, xbreak, y, state, fcnUt, fcnBc):
    """ Solves a system of partial differential equations of the form ut = f(x, t, u, ux, uxx) using the method of lines. The solution is represented with cubic Hermite polynomials.
    """
    if (state[0] is None) or (state[0].state is None):
        errStr = Translator.getString("pdemlnotavailable")
        raise ValueError(errStr)
    if (not(isinstance(state[0], CnlState))):
        errStr = Translator.getString("statecorrupt")
        raise ValueError(errStr)
    imslmath.imsl_d_pde_method_of_lines.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_pde_method_of_lines('
    evalstring += 'c_int(npdes)'
    evalstring += ','
    t_tmp = t[0]
    if (not(isinstance(t_tmp, c_double))):
        t_tmp = c_double(t[0])
    evalstring += 'byref(t_tmp)'
    evalstring += ','

    evalstring += 'c_double(tend)'
    evalstring += ','
    evalstring += 'c_int(nx)'
    evalstring += ','
    xbreak = toNumpyArray(xbreak, 'xbreak', shape=shape,
                          dtype='double', expectedShape=(0))
    evalstring += 'xbreak.ctypes.data_as(c_void_p)'
    nx = shape[0]
    evalstring += ','
    y_tmp = y
    if (not(isinstance(y_tmp, ndarray))):
        y_tmp = toNumpyArray(y_tmp, 'y', shape=shape,
                             dtype='double', expectedShape=(0, nx))
    evalstring += 'y_tmp.ctypes.data_as(c_void_p)'
    npdes = len(y_tmp)
    evalstring += ','
    evalstring += 'state[0].state'
    evalstring += ','
    checkForCallable(fcnUt, 'fcnUt')
    TMP_FCNUT = CFUNCTYPE(c_void_p, c_int, c_double, c_double, POINTER(
        c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double))
    tmp_fcnUt = TMP_FCNUT(fcnUt)
    state.append(tmp_fcnUt)
    evalstring += 'tmp_fcnUt'
    evalstring += ','
    checkForCallable(fcnBc, 'fcnBc')
    TMP_FCNBC = CFUNCTYPE(c_void_p, c_int, c_double, c_double, POINTER(
        c_double), POINTER(c_double), POINTER(c_double))
    tmp_fcnBc = TMP_FCNBC(fcnBc)
    state.append(tmp_fcnBc)
    evalstring += 'tmp_fcnBc'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(t_tmp, inout=True, shape=(1), pyvar=t)
    processRet(y_tmp, inout=True, shape=(npdes, nx), pyvar=y)
    return
