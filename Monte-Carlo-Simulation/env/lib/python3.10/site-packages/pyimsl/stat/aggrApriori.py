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
from pyimsl.util.imslUtils import *
from numpy import array, empty
from ctypes import *
from .statStructs import Imsls_d_apriori_itemsets
from .statStructs import Imsls_d_association_rules

IMSLS_FREQUENT_ITEMSETS = 50905
IMSLS_UNION = 50906
IMSLS_COUNT = 50907
IMSLS_SUM = 50908
IMSLS_UPDATE_FREQ_ITEMSETS = 50909
IMSLS_ASSOCIATION_RULES = 50904
imslstat = loadimsl(STAT)


def aggrApriori(frequentItemsets=None, union=None, count=None, sum=None, updateFreqItemsets=None, associationRules=None):
    """ Computes the frequent itemsets in a transaction set using aggregation.
    """
    imslstat.imsls_d_aggr_apriori.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_aggr_apriori('
    # evalstring +='c_int(step)'
    if not (frequentItemsets is None):
        # evalstring +=','
        evalstring += repr(IMSLS_FREQUENT_ITEMSETS)
        checkForDict(frequentItemsets, 'frequentItemsets', [
                     'x', 'maxNumProducts', 'maxSetSize', 'minPctSupport'])
        evalstring += ','
        evalstring += 'c_int(frequentItemsets_n_tmp)'
        evalstring += ','
        frequentItemsets_x_tmp = frequentItemsets['x']
        frequentItemsets_x_tmp = toNumpyArray(
            frequentItemsets_x_tmp, 'x', shape=shape, dtype='int', expectedShape=(0, 2))
        evalstring += 'frequentItemsets_x_tmp.ctypes.data_as(c_void_p)'
        frequentItemsets_n_tmp = shape[0]
        evalstring += ','
        frequentItemsets_maxNumProducts_tmp = frequentItemsets['maxNumProducts']
        evalstring += 'c_int(frequentItemsets_maxNumProducts_tmp)'
        evalstring += ','
        frequentItemsets_maxSetSize_tmp = frequentItemsets['maxSetSize']
        evalstring += 'c_int(frequentItemsets_maxSetSize_tmp)'
        evalstring += ','
        frequentItemsets_minPctSupport_tmp = frequentItemsets['minPctSupport']
        evalstring += 'c_double(frequentItemsets_minPctSupport_tmp)'
        evalstring += ','
        # frequentItemsets_itemsets_tmp = struct(struct())
        # evalstring += 'byref(frequentItemsets_itemsets_tmp)'
        frequentItemsets_itemsets_tmp = POINTER(
            Imsls_d_apriori_itemsets)(Imsls_d_apriori_itemsets())
        evalstring += 'byref(frequentItemsets_itemsets_tmp)'
    if not (union is None):
        # evalstring +=','
        evalstring += repr(IMSLS_UNION)
        checkForDict(union, 'union', ['itemsets1', 'itemsets2'])
        evalstring += ','
        union_itemsets1_tmp = union['itemsets1']
        # union_itemsets1_tmp = toNumpyArray(union_itemsets1_tmp, 'itemsets1', shape=shape, dtype='struct', expectedShape=(1))
        # evalstring +='union_itemsets1_tmp.ctypes.data_as(c_void_p)'
        evalstring += 'union_itemsets1_tmp'
        evalstring += ','
        union_itemsets2_tmp = union['itemsets2']
        # union_itemsets2_tmp = toNumpyArray(union_itemsets2_tmp, 'itemsets2', shape=shape, dtype='struct', expectedShape=(1))
        # evalstring +='union_itemsets2_tmp.ctypes.data_as(c_void_p)'
        evalstring += 'union_itemsets2_tmp'
        evalstring += ','
        # union_candItemsets_tmp = struct(struct())
        # evalstring += 'byref(union_candItemsets_tmp)'
        union_candItemsets_tmp = POINTER(
            Imsls_d_apriori_itemsets)(Imsls_d_apriori_itemsets())
        evalstring += 'byref(union_candItemsets_tmp)'
    if not (count is None):
        # evalstring +=','
        evalstring += repr(IMSLS_COUNT)
        checkForDict(count, 'count', ['candItemsets', 'x'])
        evalstring += ','
        count_candItemsets_tmp = count['candItemsets']
        # count_candItemsets_tmp = toNumpyArray(count_candItemsets_tmp, 'candItemsets', shape=shape, dtype='struct', expectedShape=(1))
        # evalstring +='count_candItemsets_tmp.ctypes.data_as(c_void_p)'
        evalstring += 'count_candItemsets_tmp'
        evalstring += ','
        evalstring += 'c_int(count_n_tmp)'
        evalstring += ','
        count_x_tmp = count['x']
        count_x_tmp = toNumpyArray(
            count_x_tmp, 'x', shape=shape, dtype='int', expectedShape=(0, 2))
        evalstring += 'count_x_tmp.ctypes.data_as(c_void_p)'
        count_n_tmp = shape[0]
        evalstring += ','
        count_freq_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(count_freq_tmp)'
    if not (sum is None):
        # evalstring +=','
        evalstring += repr(IMSLS_SUM)
        checkForDict(sum, 'sum', ['prevFreq1', 'prevFreq2'])
        evalstring += ','
        evalstring += 'c_int(sum_nItemsets_tmp)'
        evalstring += ','
        sum_prevFreq1_tmp = sum['prevFreq1']
        sum_prevFreq1_tmp = toNumpyArray(
            sum_prevFreq1_tmp, 'prevFreq1', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'sum_prevFreq1_tmp.ctypes.data_as(c_void_p)'
        sum_nItemsets_tmp = shape[0]
        evalstring += ','
        sum_prevFreq2_tmp = sum['prevFreq2']
        sum_prevFreq2_tmp = toNumpyArray(
            sum_prevFreq2_tmp, 'prevFreq2', shape=shape, dtype='int', expectedShape=(sum_nItemsets_tmp))
        evalstring += 'sum_prevFreq2_tmp.ctypes.data_as(c_void_p)'
        evalstring += ','
        sum_freq_tmp = POINTER(c_int)(c_int())
        evalstring += 'byref(sum_freq_tmp)'
    if not (updateFreqItemsets is None):
        # evalstring +=','
        evalstring += repr(IMSLS_UPDATE_FREQ_ITEMSETS)
        checkForDict(updateFreqItemsets, 'updateFreqItemsets',
                     ['candItemsets', 'freq'])
        evalstring += ','
        updateFreqItemsets_candItemsets_tmp = updateFreqItemsets['candItemsets']
        # updateFreqItemsets_candItemsets_tmp = toNumpyArray(updateFreqItemsets_candItemsets_tmp, 'candItemsets', shape=shape, dtype='struct', expectedShape=(1))
        # evalstring +='updateFreqItemsets_candItemsets_tmp.ctypes.data_as(c_void_p)'
        evalstring += 'updateFreqItemsets_candItemsets_tmp'
        evalstring += ','
        evalstring += 'c_int(updateFreqItemsets_nItemsets_tmp)'
        evalstring += ','
        updateFreqItemsets_freq_tmp = updateFreqItemsets['freq']
        updateFreqItemsets_freq_tmp = toNumpyArray(
            updateFreqItemsets_freq_tmp, 'freq', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'updateFreqItemsets_freq_tmp.ctypes.data_as(c_void_p)'
        updateFreqItemsets_nItemsets_tmp = shape[0]
        evalstring += ','
        # updateFreqItemsets_itemsets_tmp = struct(struct())
        # evalstring += 'byref(updateFreqItemsets_itemsets_tmp)'
        updateFreqItemsets_itemsets_tmp = POINTER(
            Imsls_d_apriori_itemsets)(Imsls_d_apriori_itemsets())
        evalstring += 'byref(updateFreqItemsets_itemsets_tmp)'
    if not (associationRules is None):
        # evalstring +=','
        evalstring += repr(IMSLS_ASSOCIATION_RULES)
        checkForDict(associationRules, 'associationRules',
                     ['itemsets', 'confidence', 'lift'])
        evalstring += ','
        associationRules_itemsets_tmp = associationRules['itemsets']
        # associationRules_itemsets_tmp = toNumpyArray(associationRules_itemsets_tmp, 'itemsets', shape=shape, dtype='struct', expectedShape=(1))
        # evalstring +='associationRules_itemsets_tmp.ctypes.data_as(c_void_p)'
        evalstring += 'associationRules_itemsets_tmp'
        evalstring += ','
        associationRules_confidence_tmp = associationRules['confidence']
        evalstring += 'c_double(associationRules_confidence_tmp)'
        evalstring += ','
        associationRules_lift_tmp = associationRules['lift']
        evalstring += 'c_double(associationRules_lift_tmp)'
        evalstring += ','
        # associationRules_assocRules_tmp = struct(struct())
        # evalstring += 'byref(associationRules_assocRules_tmp)'
        associationRules_assocRules_tmp = POINTER(
            Imsls_d_association_rules)(Imsls_d_association_rules())
        evalstring += 'byref(associationRules_assocRules_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (frequentItemsets is None):
        #        processRet(frequentItemsets_itemsets_tmp, shape=(1), key='itemsets', pyvar=frequentItemsets)
        frequentItemsets["itemsets"] = frequentItemsets_itemsets_tmp
    if not (union is None):
        #        processRet(union_candItemsets_tmp, shape=(1), key='candItemsets', pyvar=union)
        union["candItemsets"] = union_candItemsets_tmp
    if not (count is None):
        # custom code: need to get length of count from input structure.
        nCount = count_candItemsets_tmp[0].n_itemsets
        processRet(count_freq_tmp, shape=nCount, key='freq', pyvar=count)
    if not (sum is None):
        processRet(sum_freq_tmp, shape=(
            sum_nItemsets_tmp), key='freq', pyvar=sum)
    if not (updateFreqItemsets is None):
        #        processRet(updateFreqItemsets_itemsets_tmp, shape=(1), key='itemsets', pyvar=updateFreqItemsets)
        updateFreqItemsets["itemsets"] = updateFreqItemsets_itemsets_tmp
    if not (associationRules is None):
        #        processRet(associationRules_assocRules_tmp, shape=(1), key='assocRules', pyvar=associationRules)
        associationRules["assocRules"] = associationRules_assocRules_tmp
    return
