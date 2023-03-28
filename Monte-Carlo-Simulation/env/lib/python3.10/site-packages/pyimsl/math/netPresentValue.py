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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import c_double, c_int, c_void_p

imslmath = loadimsl(MATH)


def netPresentValue(rate, values):
    """ Evaluates the net present value of a stream of unequal periodic cash flows, which are subject to a given discount rate.
    """
    imslmath.imsl_d_net_present_value.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_net_present_value('
    evalstring += 'c_double(rate)'
    evalstring += ','
    evalstring += 'c_int(count)'
    evalstring += ','
    values = toNumpyArray(values, 'values', shape=shape,
                          dtype='double', expectedShape=(0))
    evalstring += 'values.ctypes.data_as(c_void_p)'
    count = shape[0]
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
