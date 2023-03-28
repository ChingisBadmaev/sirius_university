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
from pyimsl.util.imslUtils import STAT, checkForList, checkForDict, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from numpy import double, dtype, shape
from ctypes import POINTER, byref, c_double, c_int, c_void_p

IMSLS_METHOD = 13170
IMSLS_TRANSFORMATION = 40307
IMSLS_CLUSTERS = 40300
imslstat = loadimsl(STAT)


def clusterHierarchical(dist, method=None, transformation=None, clusters=None):
    """ Performs a hierarchical cluster analysis given a distance matrix.
    """
    imslstat.imsls_d_cluster_hierarchical.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_cluster_hierarchical('
    evalstring += 'c_int(npt)'
    evalstring += ','
    dist_tmp = toNumpyArray(dist, 'dist', shape=shape,
                            dtype='double', expectedShape=(0, 0))
    evalstring += 'dist_tmp.ctypes.data_as(c_void_p)'
    npt = shape[0]
    if not (method is None):
        evalstring += ','
        evalstring += repr(IMSLS_METHOD)
        evalstring += ','
        evalstring += 'c_int(method)'
    if not (transformation is None):
        evalstring += ','
        evalstring += repr(IMSLS_TRANSFORMATION)
        evalstring += ','
        evalstring += 'c_int(transformation)'
    if not (clusters is None):
        evalstring += ','
        evalstring += repr(IMSLS_CLUSTERS)
        checkForDict(clusters, 'clusters', [])
        evalstring += ','
        clusters_clevel_tmp = POINTER(c_double)(c_double())
        evalstring += 'byref(clusters_clevel_tmp)'
        evalstring += ','
        clusters_iclson_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(clusters_iclson_tmp)'
        evalstring += ','
        clusters_icrson_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(clusters_icrson_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    processRet(dist_tmp, inout=True, pyvar=dist)
    if not (clusters is None):
        processRet(clusters_clevel_tmp, shape=(npt - 1),
                   key='clevel', createArray=True, pyvar=clusters)
        processRet(clusters_iclson_tmp, shape=(npt - 1),
                   key='iclson', createArray=True, pyvar=clusters)
        processRet(clusters_icrson_tmp, shape=(npt - 1),
                   key='icrson', createArray=True, pyvar=clusters)
    return
