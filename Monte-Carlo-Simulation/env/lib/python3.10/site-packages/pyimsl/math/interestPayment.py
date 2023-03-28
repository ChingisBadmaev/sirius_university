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

AT_END_OF_PERIOD = 0
AT_BEGINNING_OF_PERIOD = 1

imslmath = loadimsl(MATH)


def interestPayment(rate, period, nPeriods, presentValue, futureValue, when):
    """ Evaluates the interest payment for an investment for a given period.
    """
    imslmath.imsl_d_interest_payment.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_interest_payment('
    evalstring += 'c_double(rate)'
    evalstring += ','
    evalstring += 'c_int(period)'
    evalstring += ','
    evalstring += 'c_int(nPeriods)'
    evalstring += ','
    evalstring += 'c_double(presentValue)'
    evalstring += ','
    evalstring += 'c_double(futureValue)'
    evalstring += ','
    evalstring += 'c_int(when)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
