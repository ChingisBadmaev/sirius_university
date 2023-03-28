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
from ctypes import c_int
from .mathStructs import tm
from .mathStructs import tm

DAY_CNT_BASIS_ACTUALACTUAL = 0
DAY_CNT_BASIS_NASD = 1
DAY_CNT_BASIS_ACTUAL360 = 2
DAY_CNT_BASIS_ACTUAL365 = 3
DAY_CNT_BASIS_30E360 = 4

ANNUAL = 1
SEMIANNUAL = 2
QUARTERLY = 4

imslmath = loadimsl(MATH)


def couponNumber(settlement, maturity, frequency, basis):
    """ Evaluates the number of coupons payable between the settlement date and the maturity date.
    """
    imslmath.imsl_coupon_number.restype = c_int
    shape = []
    evalstring = 'imslmath.imsl_coupon_number('
    evalstring += 'settlement'
    evalstring += ','
    evalstring += 'maturity'
    evalstring += ','
    evalstring += 'c_int(frequency)'
    evalstring += ','
    evalstring += 'c_int(basis)'
    evalstring += ')'
    settlement = dateConvert(settlement, toStructTm=True)
    maturity = dateConvert(maturity, toStructTm=True)
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
