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
from pyimsl.util.imslUtils import MATH, dateConvert, fatalErrorCheck, loadimsl
from numpy import shape
from ctypes import c_double
from .mathStructs import tm
from .mathStructs import tm

imslmath = loadimsl(MATH)


def treasuryBillYield(settlement, maturity, price):
    """ Evaluates the yield of a Treasury bill.
    """
    imslmath.imsl_d_treasury_bill_yield.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_treasury_bill_yield('
    evalstring += 'settlement'
    evalstring += ','
    evalstring += 'maturity'
    evalstring += ','
    evalstring += 'c_double(price)'
    evalstring += ')'
    settlement = dateConvert(settlement, toStructTm=True)
    maturity = dateConvert(maturity, toStructTm=True)
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
