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
from pyimsl.util.imslUtils import MATH, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import byref, c_int

imslmath = loadimsl(MATH)


def daysToDate(days, day, month, year):
    """ Gives the date corresponding to the number of days since January 1, 1900.
    """
    imslmath.imsl_days_to_date.restype = None
    shape = []
    evalstring = 'imslmath.imsl_days_to_date('
    evalstring += 'c_int(days)'
    evalstring += ','
    day_tmp = c_int()
    evalstring += 'byref(day_tmp)'
    evalstring += ','
    month_tmp = c_int()
    evalstring += 'byref(month_tmp)'
    evalstring += ','
    year_tmp = c_int()
    evalstring += 'byref(year_tmp)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    processRet(day_tmp, shape=1, pyvar=day)
    processRet(month_tmp, shape=1, pyvar=month)
    processRet(year_tmp, shape=1, pyvar=year)
    return
