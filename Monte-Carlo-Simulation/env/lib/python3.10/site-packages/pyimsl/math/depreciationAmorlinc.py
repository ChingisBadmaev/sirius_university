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
from ctypes import c_double, c_int
from .mathStructs import tm
from .mathStructs import tm

DAY_CNT_BASIS_ACTUALACTUAL = 0
DAY_CNT_BASIS_NASD = 1
DAY_CNT_BASIS_ACTUAL360 = 2
DAY_CNT_BASIS_ACTUAL365 = 3
DAY_CNT_BASIS_30E360 = 4

imslmath = loadimsl(MATH)


def depreciationAmorlinc(cost, issue, firstPeriod, salvage, period, rate, basis):
    """ Evaluates the depreciation for each accounting period. This function is similar to depreciation_amordegrc, except that depreciation_amordegrc has a depreciation coefficient that is applied during the evaluation that is based on the asset life.
    """
    imslmath.imsl_d_depreciation_amorlinc.restype = c_double
    shape = []
    evalstring = 'imslmath.imsl_d_depreciation_amorlinc('
    evalstring += 'c_double(cost)'
    evalstring += ','
    evalstring += 'issue'
    evalstring += ','
    evalstring += 'firstPeriod'
    evalstring += ','
    evalstring += 'c_double(salvage)'
    evalstring += ','
    evalstring += 'c_int(period)'
    evalstring += ','
    evalstring += 'c_double(rate)'
    evalstring += ','
    evalstring += 'c_int(basis)'
    evalstring += ')'
    issue = dateConvert(issue, toStructTm=True)
    firstPeriod = dateConvert(firstPeriod, toStructTm=True)
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return result
