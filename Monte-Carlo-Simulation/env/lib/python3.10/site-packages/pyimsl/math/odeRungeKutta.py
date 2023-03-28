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
from ctypes import CFUNCTYPE, POINTER, byref, c_double, c_int, c_void_p
from pyimsl.math.OdeRKState import OdeRKState
from pyimsl.util.Translator import Translator

imslmath = loadimsl(MATH)


def odeRungeKutta(t, tend, y, state, fcn):
    """ Solves an initial-value problem for ordinary differential equations using the  Runge-Kutta-Verner fifth-order and sixth-order method.
    """
    if (state[0] is None) or (state[0].state is None):
        errStr = Translator.getString("orknotavailable")
        raise ValueError(errStr)
    if (not(isinstance(state[0], OdeRKState))):
        errStr = Translator.getString("statecorrupt")
        raise ValueError(errStr)
    imslmath.imsl_d_ode_runge_kutta.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_ode_runge_kutta('
    evalstring += 'c_int(neq)'
    evalstring += ','
    t_tmp = c_double(t[0])
    evalstring += 'byref(t_tmp)'
    evalstring += ','
    evalstring += 'c_double(tend)'
    evalstring += ','
    y_tmp = toNumpyArray(y, 'y', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'y_tmp.ctypes.data_as(c_void_p)'
    neq = shape[0]
    evalstring += ','
    evalstring += 'state[0].state'
    evalstring += ','
    checkForCallable(fcn, 'fcn')
    TMP_FCN = CFUNCTYPE(c_void_p, c_int, c_double,
                        POINTER(c_double), POINTER(c_double))
    tmp_fcn = TMP_FCN(fcn)

    # keep a reference to the fcn in case it is used by the state variable
    state.append(fcn)
    state.append(tmp_fcn)
    evalstring += 'tmp_fcn'
    evalstring += ')'

    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(y_tmp, shape=(neq), pyvar=y, inout=True)
    processRet(t_tmp, shape=(1), pyvar=t, inout=True)
    return
