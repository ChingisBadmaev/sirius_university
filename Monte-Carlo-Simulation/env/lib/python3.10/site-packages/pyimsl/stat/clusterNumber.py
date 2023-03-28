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
from numpy import dtype, int, shape
from ctypes import POINTER, byref, c_int, c_void_p

IMSLS_OBS_PER_CLUSTER = 40304
imslstat = loadimsl(STAT)


def clusterNumber(npt, iclson, icrson, k, obsPerCluster=None):
    """ Computes cluster membership for a hierarchical cluster tree.
    """
    imslstat.imsls_cluster_number.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_cluster_number('
    evalstring += 'c_int(npt)'
    evalstring += ','
    iclson = toNumpyArray(iclson, 'iclson', shape=shape,
                          dtype='int', expectedShape=(npt - 1))
    evalstring += 'iclson.ctypes.data_as(c_void_p)'
    evalstring += ','
    icrson = toNumpyArray(icrson, 'icrson', shape=shape,
                          dtype='int', expectedShape=(npt - 1))
    evalstring += 'icrson.ctypes.data_as(c_void_p)'
    evalstring += ','
    evalstring += 'c_int(k)'
    if not (obsPerCluster is None):
        evalstring += ','
        evalstring += repr(IMSLS_OBS_PER_CLUSTER)
        checkForList(obsPerCluster, 'obsPerCluster')
        evalstring += ','
        obsPerCluster_obsPerCluster_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(obsPerCluster_obsPerCluster_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (obsPerCluster is None):
        processRet(obsPerCluster_obsPerCluster_tmp,
                   shape=(k), pyvar=obsPerCluster)
    return processRet(result, shape=(npt), result=True)
