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
from pyimsl.util.imslUtils import MATH, checkForBoolean, checkForList, fatalErrorCheck, loadimsl, processRet
from numpy import cosh, empty, shape, size
from ctypes import c_double, c_int, c_void_p

IMSL_CHEBYSHEV_FIRST = 10240
IMSL_CHEBYSHEV_SECOND = 10241
IMSL_HERMITE = 10242
IMSL_COSH = 10243
IMSL_JACOBI = 10244
IMSL_GEN_LAGUERRE = 10245
IMSL_FIXED_POINT = 10246
IMSL_TWO_FIXED_POINTS = 10247
imslmath = loadimsl(MATH)


def gaussQuadRule(quadpts, weights, points, chebyshevFirst=None, chebyshevSecond=None, hermite=None, cosh=None, jacobi=None, genLaguerre=None, fixedPoint=None, twoFixedPoints=None):
    """ Computes a Gauss, Gauss-Radau, or Gauss-Lobatto quadrature rule with various classical weight functions.
    """
    imslmath.imsl_d_gauss_quad_rule.restype = None
    shape = []
    evalstring = 'imslmath.imsl_d_gauss_quad_rule('
    evalstring += 'c_int(quadpts)'
    evalstring += ','
    weights_tmp = empty(quadpts)
    evalstring += 'weights_tmp.ctypes.data_as(c_void_p)'
    evalstring += ','
    points_tmp = empty(quadpts)
    evalstring += 'points_tmp.ctypes.data_as(c_void_p)'
    checkForBoolean(chebyshevFirst, 'chebyshevFirst')
    if (chebyshevFirst):
        evalstring += ','
        evalstring += repr(IMSL_CHEBYSHEV_FIRST)
    checkForBoolean(chebyshevSecond, 'chebyshevSecond')
    if (chebyshevSecond):
        evalstring += ','
        evalstring += repr(IMSL_CHEBYSHEV_SECOND)
    checkForBoolean(hermite, 'hermite')
    if (hermite):
        evalstring += ','
        evalstring += repr(IMSL_HERMITE)
    checkForBoolean(cosh, 'cosh')
    if (cosh):
        evalstring += ','
        evalstring += repr(IMSL_COSH)
    if not (jacobi is None):
        evalstring += ','
        evalstring += repr(IMSL_JACOBI)
        checkForDict(jacobi, 'jacobi', ['alpha', 'beta'])
        evalstring += ','
        jacobi_alpha_tmp = jacobi['alpha']
        evalstring += 'c_double(jacobi_alpha_tmp)'
        evalstring += ','
        jacobi_beta_tmp = jacobi['beta']
        evalstring += 'c_double(jacobi_beta_tmp)'
    if not (genLaguerre is None):
        evalstring += ','
        evalstring += repr(IMSL_GEN_LAGUERRE)
        evalstring += ','
        evalstring += 'c_double(genLaguerre)'
    if not (fixedPoint is None):
        evalstring += ','
        evalstring += repr(IMSL_FIXED_POINT)
        evalstring += ','
        evalstring += 'c_double(fixedPoint)'
    if not (twoFixedPoints is None):
        evalstring += ','
        evalstring += repr(IMSL_TWO_FIXED_POINTS)
        checkForDict(twoFixedPoints, 'twoFixedPoints', ['a', 'b'])
        evalstring += ','
        twoFixedPoints_a_tmp = twoFixedPoints['a']
        evalstring += 'c_double(twoFixedPoints_a_tmp)'
        evalstring += ','
        twoFixedPoints_b_tmp = twoFixedPoints['b']
        evalstring += 'c_double(twoFixedPoints_b_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if isinstance(weights, list):
        weights[:] = []
    processRet(weights_tmp, shape=(quadpts), pyvar=weights)
    if isinstance(points, list):
        points[:] = []
    processRet(points_tmp, shape=(quadpts), pyvar=points)
    return
