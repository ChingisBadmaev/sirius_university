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

IMSLS_MAX_SET_SIZE = 50901
IMSLS_MIN_SUPPORT = 50902
IMSLS_ASSOCIATION_RULES = 50904
imslstat = loadimsl(STAT)


def apriori(x, maxNumProducts, maxSetSize=None, minSupport=None, associationRules=None):
    """ Computes the frequent itemsets in a transaction set.
    """
    # imslstat.imsls_d_apriori.restype = struct
    imslstat.imsls_d_apriori.restype = POINTER(Imsls_d_apriori_itemsets)
    shape = []
    evalstring = 'imslstat.imsls_d_apriori('
    evalstring += 'c_int(n)'
    evalstring += ','
    x = toNumpyArray(x, 'x', shape=shape, dtype='int', expectedShape=(0, 2))
    evalstring += 'x.ctypes.data_as(c_void_p)'
    n = shape[0]
    evalstring += ','
    evalstring += 'c_int(maxNumProducts)'
    if not (maxSetSize is None):
        evalstring += ','
        evalstring += repr(IMSLS_MAX_SET_SIZE)
        evalstring += ','
        evalstring += 'c_int(maxSetSize)'
    if not (minSupport is None):
        evalstring += ','
        evalstring += repr(IMSLS_MIN_SUPPORT)
        evalstring += ','
        evalstring += 'c_double(minSupport)'
    if not (associationRules is None):
        evalstring += ','
        evalstring += repr(IMSLS_ASSOCIATION_RULES)
        checkForDict(associationRules, 'associationRules',
                     ['confidence', 'lift'])
        evalstring += ','
        associationRules_confidence_tmp = associationRules['confidence']
        evalstring += 'c_double(associationRules_confidence_tmp)'
        evalstring += ','
        associationRules_lift_tmp = associationRules['lift']
        evalstring += 'c_double(associationRules_lift_tmp)'
        evalstring += ','
        associationRules_assocRules_tmp = POINTER(
            Imsls_d_association_rules)(Imsls_d_association_rules())
        evalstring += 'byref(associationRules_assocRules_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (associationRules is None):
        associationRules["assocRules"] = associationRules_assocRules_tmp
    return result
