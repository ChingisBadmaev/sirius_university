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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl
from numpy import shape
from ctypes import c_double

imslstat = loadimsl(STAT)


def logGamma(x):
    """ Evaluates the logarithm of the absolute value of a gamma function log.
    """
    imslstat.imsls_d_log_gamma.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_log_gamma('
    evalstring += 'c_double(x)'
    evalstring += ')'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return result
