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
from pyimsl.util.VersionFacade import VersionFacade

IMSL_DERIV = 10028
imslmath = loadimsl(MATH)


def feynmanKacEvaluate(breakpoints, w, coef, deriv=None):
    VersionFacade.checkVersion(7)
    imslmath.imsl_d_feynman_kac_evaluate.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_feynman_kac_evaluate('
    evalstring += 'c_int(nw)'
    evalstring += ','
    evalstring += 'c_int(m)'
    evalstring += ','
    breakpoints = toNumpyArray(
        breakpoints, 'breakpoints', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'breakpoints.ctypes.data_as(c_void_p)'
    m = shape[0]
    evalstring += ','
    w = toNumpyArray(w, 'w', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'w.ctypes.data_as(c_void_p)'
    nw = shape[0]
    evalstring += ','
    coef = toNumpyArray(coef, 'coef', shape=shape,
                        dtype='double', expectedShape=(3 * m))
    evalstring += 'coef.ctypes.data_as(c_void_p)'
    if not (deriv is None):
        evalstring += ','
        evalstring += repr(IMSL_DERIV)
        evalstring += ','
        evalstring += 'c_int(deriv)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(nw), result=True)
