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
from numpy import shape, double, float
from ctypes import c_float

# Note: A bug in imsl_d_erfce prevents this from working properly so the float version
#       is used until this can be corrected in CNL.
imslmath = loadimsl(MATH)


def erfce(x):
    """ Evaluates the exponentially scaled complementary error function.
    """
    fx = float(x)
    imslmath.imsl_f_erfce.restype = c_float
    shape = []
    evalstring = 'imslmath.imsl_f_erfce('
    evalstring += 'c_float(fx)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return double(result)
