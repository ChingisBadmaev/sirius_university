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

imslstat = loadimsl(STAT)


def geometricInverseCdf(p, pin):
    """ Evaluates the inverse of the discrete geometric cumulative distribution function.
    """
    imslstat.imsls_d_geometric_inverse_cdf.restype = c_int
    shape = []
    evalstring = 'imslstat.imsls_d_geometric_inverse_cdf('
    evalstring += 'c_double(p)'
    evalstring += ','
    evalstring += 'c_double(pin)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return result
