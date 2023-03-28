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
from pyimsl.util.imslUtils import MATH, date, fatalErrorCheck, loadimsl, toNumpyArray
from numpy import double, dtype, shape
from ctypes import c_double, c_int, c_void_p
from .mathStructs import tm

IMSL_XGUESS = 10100
IMSL_HIGHEST = 10224
imslmath = loadimsl(MATH)


def internalRateSchedule(values, dates, xguess=None, highest=None):
    """ Evaluates the internal rate of return for a schedule of cash flows. It is not necessary that the cash flows be periodic.
    """
    imslmath.imsl_d_internal_rate_schedule.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_internal_rate_schedule('
    evalstring += 'c_int(count)'
    evalstring += ','
    values = toNumpyArray(values, 'values', shape=shape,
                          dtype='double', expectedShape=(0))
    evalstring += 'values.ctypes.data_as(c_void_p)'
    count = shape[0]
    evalstring += ','
    dates = toNumpyArray(dates, 'dates', shape=shape,
                         dtype='date', expectedShape=(count))
    evalstring += 'dates'
    if not (xguess is None):
        evalstring += ','
        evalstring += repr(IMSL_XGUESS)
        evalstring += ','
        evalstring += 'c_double(xguess)'
    if not (highest is None):
        evalstring += ','
        evalstring += repr(IMSL_HIGHEST)
        evalstring += ','
        evalstring += 'c_double(highest)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
