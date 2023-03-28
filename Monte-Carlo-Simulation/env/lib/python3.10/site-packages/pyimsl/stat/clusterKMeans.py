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
from pyimsl.util.imslUtils import STAT, checkForList, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, int, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_WEIGHTS = 15400
IMSLS_FREQUENCIES = 11790
IMSLS_MAX_ITERATIONS = 12970
IMSLS_CLUSTER_MEANS = 10640
IMSLS_CLUSTER_MEANS_USER = 15740
IMSLS_CLUSTER_SSQ = 10660
IMSLS_CLUSTER_SSQ_USER = 10670
IMSLS_X_COL_DIM = 15470
IMSLS_CLUSTER_MEANS_COL_DIM = 15730
IMSLS_CLUSTER_SEEDS_COL_DIM = 15720
IMSLS_CLUSTER_COUNTS = 15760
IMSLS_CLUSTER_COUNTS_USER = 15770
IMSLS_CLUSTER_VARIABLE_COLUMNS = 15750
IMSLS_CLUSTER_HISTORY = 50983
imslstat = loadimsl(STAT)


def clusterKMeans(nVariables, x, clusterSeeds, weights=None, frequencies=None, maxIterations=None, clusterMeans=None, clusterSsq=None, xColDim=None, clusterMeansColDim=None, clusterSeedsColDim=None, clusterCounts=None, clusterVariableColumns=None, clusterHistory=None):
    """ Performs a K-means (centroid) cluster analysis.
    """
    imslstat.imsls_d_cluster_k_means.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_d_cluster_k_means('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nVariables)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                     expectedShape=((0, 0)))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    nObservations = shape[0]
    # nVariables=shape[1] # must be passed in as columns can be skiped
    evalstring += ','
    evalstring += 'c_int(nClusters)'
    evalstring += ','
    clusterSeeds = toNumpyArray(clusterSeeds, 'clusterSeeds',
                                shape=shape, dtype='double', expectedShape=((0, nVariables)))
    evalstring += 'clusterSeeds.ctypes.data_as(c_void_p)'
    nClusters = shape[0]
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(
            weights, 'weights', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='double', expectedShape=(nObservations))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (maxIterations is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_ITERATIONS)
        evalstring += ','
        evalstring += 'c_int(maxIterations)'
    if not (clusterMeans is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLUSTER_MEANS_USER)
        checkForList(clusterMeans, 'clusterMeans')
        evalstring += ','
        clusterMeans_clusterMeans_tmp = (c_double * (nClusters * nVariables))()
        evalstring += 'clusterMeans_clusterMeans_tmp'
    if not (clusterSsq is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLUSTER_SSQ_USER)
        checkForList(clusterSsq, 'clusterSsq')
        evalstring += ','
        clusterSsq_clusterSsq_tmp = (c_double * nClusters)()
        evalstring += 'clusterSsq_clusterSsq_tmp'
    if not (xColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(xColDim)'
    if not (clusterMeansColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLUSTER_MEANS_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(clusterMeansColDim)'
    if not (clusterSeedsColDim is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLUSTER_SEEDS_COL_DIM)
        evalstring += ','
        evalstring += 'c_int(clusterSeedsColDim)'
    if not (clusterCounts is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLUSTER_COUNTS_USER)
        checkForList(clusterCounts, 'clusterCounts')
        evalstring += ','
        clusterCounts_clusterCounts_tmp = (c_int * nClusters)()
        evalstring += 'clusterCounts_clusterCounts_tmp'
    if not (clusterVariableColumns is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLUSTER_VARIABLE_COLUMNS)
        evalstring += ','
        clusterVariableColumns = toNumpyArray(
            clusterVariableColumns, 'clusterVariableColumns', shape=shape, dtype='int', expectedShape=(nVariables))
        evalstring += 'clusterVariableColumns.ctypes.data_as(c_void_p)'

    if not (clusterHistory is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLUSTER_HISTORY)
        checkForList(clusterHistory, 'clusterHistory')
        evalstring += ','
        # evalstring +='c_int(clusterHistory_nItr_tmp)'
        clusterHistory_nItr_tmp = c_int()
        evalstring += 'byref(clusterHistory_nItr_tmp)'
        evalstring += ','
        clusterHistory_clusterHistory_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(clusterHistory_clusterHistory_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    # use USER versions of all return params and do not free memory from result to avoid strange crashes
    if not (clusterMeans is None):
        processRet(clusterMeans_clusterMeans_tmp, shape=(
            nClusters, nVariables), pyvar=clusterMeans, freemem=False)
    if not (clusterSsq is None):
        processRet(clusterSsq_clusterSsq_tmp, shape=(
            nClusters), pyvar=clusterSsq, freemem=False)
    if not (clusterCounts is None):
        processRet(clusterCounts_clusterCounts_tmp, shape=(
            nClusters), pyvar=clusterCounts, freemem=False)
    if not (clusterHistory is None):
        processRet(clusterHistory_clusterHistory_tmp, shape=(
            clusterHistory_nItr_tmp, nObservations), key='clusterHistory', pyvar=clusterHistory)
    return processRet(result, shape=(nObservations), result=True)
