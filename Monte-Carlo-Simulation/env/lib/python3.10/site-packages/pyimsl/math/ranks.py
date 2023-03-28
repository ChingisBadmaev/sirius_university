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
from pyimsl.util.imslUtils import MATH, checkForBoolean, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, c_double, c_int, c_void_p

IMSL_AVERAGE_TIE = 10223
IMSL_HIGHEST = 10224
IMSL_LOWEST = 10225
IMSL_RANDOM_SPLIT = 10226
IMSL_FUZZ = 10068
IMSL_RANKS = 10227
IMSL_BLOM_SCORES = 10228
IMSL_TUKEY_SCORES = 10229
IMSL_VAN_DER_WAERDEN_SCORES = 10230
IMSL_EXPECTED_NORMAL_SCORES = 10231
IMSL_SAVAGE_SCORES = 10232
imslmath = loadimsl(MATH)


def ranks(x, averageTie=None, highest=None, lowest=None, randomSplit=None, fuzz=None, ranks=None, blomScores=None, tukeyScores=None, vanDerWaerdenScores=None, expectedNormalScores=None, savageScores=None):
    """ Computes the ranks, normal scores, or exponential scores for a vector of observations.
    """
    imslmath.imsl_d_ranks.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_ranks('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    checkForBoolean(averageTie, 'averageTie')
    if (averageTie):
        evalstring += ','
        evalstring += repr(IMSL_AVERAGE_TIE)
    checkForBoolean(highest, 'highest')
    if (highest):
        evalstring += ','
        evalstring += repr(IMSL_HIGHEST)
    checkForBoolean(lowest, 'lowest')
    if (lowest):
        evalstring += ','
        evalstring += repr(IMSL_LOWEST)
    checkForBoolean(randomSplit, 'randomSplit')
    if (randomSplit):
        evalstring += ','
        evalstring += repr(IMSL_RANDOM_SPLIT)
    if not (fuzz is None):
        evalstring += ','
        evalstring += repr(IMSL_FUZZ)
        evalstring += ','
        evalstring += 'c_double(fuzz)'
    checkForBoolean(ranks, 'ranks')
    if (ranks):
        evalstring += ','
        evalstring += repr(IMSL_RANKS)
    checkForBoolean(blomScores, 'blomScores')
    if (blomScores):
        evalstring += ','
        evalstring += repr(IMSL_BLOM_SCORES)
    checkForBoolean(tukeyScores, 'tukeyScores')
    if (tukeyScores):
        evalstring += ','
        evalstring += repr(IMSL_TUKEY_SCORES)
    checkForBoolean(vanDerWaerdenScores, 'vanDerWaerdenScores')
    if (vanDerWaerdenScores):
        evalstring += ','
        evalstring += repr(IMSL_VAN_DER_WAERDEN_SCORES)
    checkForBoolean(expectedNormalScores, 'expectedNormalScores')
    if (expectedNormalScores):
        evalstring += ','
        evalstring += repr(IMSL_EXPECTED_NORMAL_SCORES)
    checkForBoolean(savageScores, 'savageScores')
    if (savageScores):
        evalstring += ','
        evalstring += repr(IMSL_SAVAGE_SCORES)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    return processRet(result, shape=(nObservations), result=True)
