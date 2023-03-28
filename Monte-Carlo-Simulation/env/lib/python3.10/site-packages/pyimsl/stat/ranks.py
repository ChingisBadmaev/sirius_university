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

IMSLS_AVERAGE_TIE = 10160
IMSLS_HIGHEST = 12190
IMSLS_LOWEST = 12860
IMSLS_RANDOM_SPLIT = 14080
IMSLS_FUZZ = 11870
IMSLS_RANKS = 14120
IMSLS_BLOM_SCORES = 10260
IMSLS_TUKEY_SCORES = 15100
IMSLS_VAN_DER_WAERDEN_SCORES = 15300
IMSLS_EXPECTED_NORMAL_SCORES = 11560
IMSLS_SAVAGE_SCORES = 14390
imslstat = loadimsl(STAT)


def ranks(x, averageTie=None, highest=None, lowest=None, randomSplit=None, fuzz=None, ranks=None, blomScores=None, tukeyScores=None, vanDerWaerdenScores=None, expectedNormalScores=None, savageScores=None):
    """ Computes the ranks, normal scores, or exponential scores for a vector of observations.
    """
    imslstat.imsls_d_ranks.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_ranks('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    checkForBoolean(averageTie, 'averageTie')
    if (averageTie):
        evalstring += ','
        evalstring += repr(IMSLS_AVERAGE_TIE)
    checkForBoolean(highest, 'highest')
    if (highest):
        evalstring += ','
        evalstring += repr(IMSLS_HIGHEST)
    checkForBoolean(lowest, 'lowest')
    if (lowest):
        evalstring += ','
        evalstring += repr(IMSLS_LOWEST)
    checkForBoolean(randomSplit, 'randomSplit')
    if (randomSplit):
        evalstring += ','
        evalstring += repr(IMSLS_RANDOM_SPLIT)
    if not (fuzz is None):
        evalstring += ','
        evalstring += repr(IMSLS_FUZZ)
        evalstring += ','
        evalstring += 'c_double(fuzz)'
    checkForBoolean(ranks, 'ranks')
    if (ranks):
        evalstring += ','
        evalstring += repr(IMSLS_RANKS)
    checkForBoolean(blomScores, 'blomScores')
    if (blomScores):
        evalstring += ','
        evalstring += repr(IMSLS_BLOM_SCORES)
    checkForBoolean(tukeyScores, 'tukeyScores')
    if (tukeyScores):
        evalstring += ','
        evalstring += repr(IMSLS_TUKEY_SCORES)
    checkForBoolean(vanDerWaerdenScores, 'vanDerWaerdenScores')
    if (vanDerWaerdenScores):
        evalstring += ','
        evalstring += repr(IMSLS_VAN_DER_WAERDEN_SCORES)
    checkForBoolean(expectedNormalScores, 'expectedNormalScores')
    if (expectedNormalScores):
        evalstring += ','
        evalstring += repr(IMSLS_EXPECTED_NORMAL_SCORES)
    checkForBoolean(savageScores, 'savageScores')
    if (savageScores):
        evalstring += ','
        evalstring += repr(IMSLS_SAVAGE_SCORES)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nObservations), result=True)
