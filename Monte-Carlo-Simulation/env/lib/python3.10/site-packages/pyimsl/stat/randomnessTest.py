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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray, checkForDict
from numpy import double, dtype, shape, size
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_RUNS = 30028
IMSLS_PAIRS = 30026
IMSLS_DSQUARE = 30024
IMSLS_DCUBE = 30022
IMSLS_RUNS_EXPECT = 30031
IMSLS_EXPECT = 30030
IMSLS_CHI_SQUARED = 10450
IMSLS_DF = 11185
IMSLS_IDO = 20440
imslstat = loadimsl(STAT)


def randomnessTest(x, nRun, runs=None, pairs=None, dsquare=None, dcube=None, runsExpect=None, expect=None, chiSquared=None, df=None, ido=None):
    """ Performs a test for randomness.
    """
    imslstat.imsls_d_randomness_test.restype = c_double
    shape = []
    evalstring = 'imslstat.imsls_d_randomness_test('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    evalstring += ','
    evalstring += 'c_int(nRun)'
    if not (runs is None):
        evalstring += ','
        evalstring += repr(IMSLS_RUNS)
        checkForDict(runs, 'runs', [])
        evalstring += ','
        runs_runsCount_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(runs_runsCount_tmp)'
        evalstring += ','
        runs_covariances_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(runs_covariances_tmp)'
    if not (pairs is None):
        evalstring += ','
        evalstring += repr(IMSLS_PAIRS)
        checkForDict(pairs, 'pairs', ['pairsLag'])
        evalstring += ','
        pairs_pairsLag_tmp = pairs['pairsLag']
        evalstring += 'c_int(pairs_pairsLag_tmp)'
        evalstring += ','
        pairs_pairsCount_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(pairs_pairsCount_tmp)'
    if not (dsquare is None):
        evalstring += ','
        evalstring += repr(IMSLS_DSQUARE)
        checkForList(dsquare, 'dsquare')
        evalstring += ','
        dsquare_dsquareCount_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(dsquare_dsquareCount_tmp)'
    if not (dcube is None):
        evalstring += ','
        evalstring += repr(IMSLS_DCUBE)
        checkForList(dcube, 'dcube')
        evalstring += ','
        dcube_dcubeCount_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(dcube_dcubeCount_tmp)'
    if not (runsExpect is None):
        evalstring += ','
        evalstring += repr(IMSLS_RUNS_EXPECT)
        checkForList(runsExpect, 'runsExpect')
        evalstring += ','
        runsExpect_runsExpect_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(runsExpect_runsExpect_tmp)'
    if not (expect is None):
        evalstring += ','
        evalstring += repr(IMSLS_EXPECT)
        checkForList(expect, 'expect')
        evalstring += ','
        expect_expect_tmp = c_double()
        evalstring += 'byref(expect_expect_tmp)'
    if not (chiSquared is None):
        evalstring += ','
        evalstring += repr(IMSLS_CHI_SQUARED)
        checkForList(chiSquared, 'chiSquared')
        evalstring += ','
        chiSquared_chiSquared_tmp = c_double()
        evalstring += 'byref(chiSquared_chiSquared_tmp)'
    if not (df is None):
        evalstring += ','
        evalstring += repr(IMSLS_DF)
        checkForList(df, 'df')
        evalstring += ','
        df_df_tmp = c_double()
        evalstring += 'byref(df_df_tmp)'
    if not (ido is None):
        evalstring += ','
        evalstring += repr(IMSLS_IDO)
        checkForDict(ido, 'ido', ['ido', 'intermediateResults'])
        evalstring += ','
        ido_tmp = ido['ido']
        evalstring += 'c_int(ido_tmp)'
        evalstring += ','
        ido_intermediateResults_tmp = ido['intermediateResults']
        expShape = (nRun)
        if not (runs is None):
            expShape = (nRun)
        if not (pairs is None):
            expShape = (nRun, nRun)
        if not (dsquare is None):
            expShape = (nRun)
        if not (dcube is None):
            expShape = (nRun, nRun, nRun)
        ido_intermediateResults_tmp = toNumpyArray(
            ido_intermediateResults_tmp, 'intermediateResults', shape=shape, dtype='double', expectedShape=expShape)
        evalstring += 'ido_intermediateResults_tmp.ctypes.data_as(c_void_p)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (runs is None):
        processRet(runs_runsCount_tmp, shape=(
            nRun), key='runsCount', pyvar=runs)
        processRet(runs_covariances_tmp, shape=(
            nRun, nRun), key='covariances', pyvar=runs)
    if not (pairs is None):
        processRet(pairs_pairsCount_tmp, shape=(
            nRun, nRun), key='pairsCount', pyvar=pairs)
    if not (dsquare is None):
        processRet(dsquare_dsquareCount_tmp, shape=(nRun), pyvar=dsquare)
    if not (dcube is None):
        processRet(dcube_dcubeCount_tmp, shape=(nRun, nRun, nRun), pyvar=dcube)
    if not (runsExpect is None):
        processRet(runsExpect_runsExpect_tmp, shape=(nRun), pyvar=runsExpect)
    if not (expect is None):
        processRet(expect_expect_tmp, shape=(1), pyvar=expect)
    if not (chiSquared is None):
        processRet(chiSquared_chiSquared_tmp, shape=(1), pyvar=chiSquared)
    if not (df is None):
        processRet(df_df_tmp, shape=(1), pyvar=df)
    if not (ido is None):
        ido["intermediateResults"] = ido_intermediateResults_tmp
    return result
