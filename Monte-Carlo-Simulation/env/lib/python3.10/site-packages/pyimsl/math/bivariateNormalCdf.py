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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl
from numpy import shape
from ctypes import c_double

imslmath = loadimsl(MATH)


def bivariateNormalCdf(x, y, rho):
    """ Evaluates the bivariate normal distribution function.
    """
    imslmath.imsl_d_bivariate_normal_cdf.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_bivariate_normal_cdf('
    evalstring += 'c_double(x)'
    evalstring += ','
    evalstring += 'c_double(y)'
    evalstring += ','
    evalstring += 'c_double(rho)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
