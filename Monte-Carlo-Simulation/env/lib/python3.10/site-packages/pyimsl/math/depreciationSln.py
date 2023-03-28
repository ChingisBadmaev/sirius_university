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
from ctypes import c_double, c_int

imslmath = loadimsl(MATH)


def depreciationSln(cost, salvage, life):
    """ Evaluates the depreciation of an asset using the straight-line method.
    """
    imslmath.imsl_d_depreciation_sln.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_depreciation_sln('
    evalstring += 'c_double(cost)'
    evalstring += ','
    evalstring += 'c_double(salvage)'
    evalstring += ','
    evalstring += 'c_int(life)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
