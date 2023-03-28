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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p
from .mathStructs import Imsl_d_radial_basis_fit

imslmath = loadimsl(MATH)


def radialEvaluate(x, radialFitState):
    """ Evaluates a radial-basis fit.
    """
    if (radialFitState[0] is None):
        errStr = Translator.getString("radialfitnotavailable")
        raise ValueError(errStr)
    imslmath.imsl_d_radial_evaluate.restype = POINTER(c_double)
    shape = []
    radialFit = radialFitState[0]
    evalstring = 'imslmath.imsl_d_radial_evaluate('
    evalstring += 'c_int(n)'
    evalstring += ','
    expectedShape = (0, radialFit[0].dimension)
    x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                     expectedShape=expectedShape)
    n = shape[0]
    evalstring += 'x.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'radialFit'
    evalstring += ',0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(n), result=True)
