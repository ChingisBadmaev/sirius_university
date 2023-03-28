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
from pyimsl.util.imslUtils import STAT, checkForBoolean, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSLS_ALPHA = 10070
IMSLS_SNK = 40180
IMSLS_LSD = 40182
IMSLS_TUKEY = 15090
IMSLS_BONFERRONI = 10270
imslstat = loadimsl(STAT)


def multipleComparisons(means, df, stdError, alpha=None, snk=None, lsd=None, tukey=None, bonferroni=None):
    """ Performs multiple comparisons of means using one of Student-Newman-Keuls, LSD, Bonferroni, Tukey's, or Duncan's MRT procedures.
    """
    imslstat.imsls_d_multiple_comparisons.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_d_multiple_comparisons('
    evalstring += 'c_int(nGroups)'
    evalstring += ','
    # NOTE: If a numpy array is passed in means, multiple_comparisons
    # WILL MODIFY ITS CONTENTS.
    means = toNumpyArray(means, 'means', shape=shape,
                         dtype='double', expectedShape=(0))
    evalstring += 'means.ctypes.data_as(c_void_p)'
    nGroups = shape[0]
    evalstring += ','
    evalstring += 'c_int(df)'
    evalstring += ','
    evalstring += 'c_double(stdError)'
    if not (alpha is None):
        evalstring += ','
        evalstring += repr(IMSLS_ALPHA)
        evalstring += ','
        evalstring += 'c_double(alpha)'
    checkForBoolean(snk, 'snk')
    if (snk):
        evalstring += ','
        evalstring += repr(IMSLS_SNK)
    checkForBoolean(lsd, 'lsd')
    if (lsd):
        evalstring += ','
        evalstring += repr(IMSLS_LSD)
    checkForBoolean(tukey, 'tukey')
    if (tukey):
        evalstring += ','
        evalstring += repr(IMSLS_TUKEY)
    checkForBoolean(bonferroni, 'bonferroni')
    if (bonferroni):
        evalstring += ','
        evalstring += repr(IMSLS_BONFERRONI)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nGroups - 1), result=True)
