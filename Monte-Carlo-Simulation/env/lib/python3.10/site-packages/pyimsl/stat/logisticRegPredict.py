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

IMSLS_Y = 15535
IMSLS_GROUP_COUNTS = 12090
IMSLS_GROUPS = 20810
IMSLS_COLUMN_WISE = 50826
IMSLS_FREQUENCIES = 11790
IMSLS_REFERENCE_CLASS = 50828
IMSLS_NO_INTERCEPT = 13350
IMSLS_X_INDICES = 20443
IMSLS_X_INTERACTIONS = 50830
IMSLS_CONFIDENCE = 10860
IMSLS_MODEL = 20100
IMSLS_PREDERR = 50831
imslstat = loadimsl(STAT)


def logisticRegPredict(nIndependent, nClasses, coefs, x, y=None, groupCounts=None, groups=None, columnWise=None, frequencies=None, referenceClass=None, noIntercept=None, xIndices=None, xInteractions=None, confidence=None, model=None, prederr=None):
    imslstat.imsls_d_logistic_reg_predict.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_logistic_reg_predict('
    evalstring += 'c_int(nObservations)'
    evalstring += ','
    evalstring += 'c_int(nIndependent)'
    evalstring += ','
    evalstring += 'c_int(nClasses)'
    evalstring += ','
    coefs = toNumpyArray(coefs, 'coefs', shape=shape,
                         dtype='double', expectedShape=(0, nClasses))
    evalstring += 'coefs.ctypes.data_as(c_void_p)'
    nCoefficients = shape[0]
    evalstring += ','
    checkForBoolean(columnWise, 'columnWise')
    if (columnWise):
        x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                         expectedShape=(nIndependent, 0))
        nObservations = shape[1]
    else:
        x = toNumpyArray(x, 'x', shape=shape, dtype='double',
                         expectedShape=(0, nIndependent))
        nObservations = shape[0]
    # x = toNumpyArray(x, 'x', shape=shape, dtype='double', expectedShape=(0,nIndependent))
    # nObservations=shape[0]
    evalstring += 'x.ctypes.data_as(c_void_p)'
    checkForBoolean(groupCounts, 'groupCounts')
    checkForBoolean(groups, 'groups')
    if not (y is None):
        if (groupCounts):
            y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                             expectedShape=(nObservations, nClasses - 1))
        elif (groups):
            y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                             expectedShape=(nObservations))
        else:
            y = toNumpyArray(y, 'y', shape=shape, dtype='double',
                             expectedShape=(nObservations, nClasses))
        evalstring += ','
        evalstring += repr(IMSLS_Y)
        evalstring += ','
        evalstring += 'y.ctypes.data_as(c_void_p)'
#    if not (y is None):
#        evalstring +=','
#        evalstring += repr(IMSLS_Y)
#        evalstring +=','
#        y = toNumpyArray(y, 'y', shape=shape, dtype='double', expectedShape=(custom code nObservations,nClasses))
#        evalstring +='y.ctypes.data_as(c_void_p)'
#    checkForBoolean(groupCounts,'groupCounts')
    if (groupCounts):
        evalstring += ','
        evalstring += repr(IMSLS_GROUP_COUNTS)
#    checkForBoolean(groups,'groups')
    if (groups):
        evalstring += ','
        evalstring += repr(IMSLS_GROUPS)
    checkForBoolean(columnWise, 'columnWise')
    if (columnWise):
        evalstring += ','
        evalstring += repr(IMSLS_COLUMN_WISE)
    if not (frequencies is None):
        evalstring += ','
        evalstring += repr(IMSLS_FREQUENCIES)
        evalstring += ','
        frequencies = toNumpyArray(
            frequencies, 'frequencies', shape=shape, dtype='float', expectedShape=(nObservations))
        evalstring += 'frequencies.ctypes.data_as(c_void_p)'
    if not (referenceClass is None):
        evalstring += ','
        evalstring += repr(IMSLS_REFERENCE_CLASS)
        evalstring += ','
        evalstring += 'c_int(referenceClass)'
    checkForBoolean(noIntercept, 'noIntercept')
    if (noIntercept):
        evalstring += ','
        evalstring += repr(IMSLS_NO_INTERCEPT)
    if not (xIndices is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_INDICES)
        evalstring += ','
        evalstring += 'c_int(xIndices_nXin_tmp)'
        evalstring += ','
        xIndices_xin_tmp = toNumpyArray(
            xIndices, 'xIndices', shape=shape, dtype='int', expectedShape=(0))
        evalstring += 'xIndices_xin_tmp.ctypes.data_as(c_void_p)'
        xIndices_nXin_tmp = shape[0]
    if not (xInteractions is None):
        evalstring += ','
        evalstring += repr(IMSLS_X_INTERACTIONS)
        evalstring += ','
        evalstring += 'c_int(xInteractions_nXinteract_tmp)'
        evalstring += ','
        xInteractions_xinteract_tmp = toNumpyArray(
            xInteractions, 'xInteractions', shape=shape, dtype='int', expectedShape=(0, 2))
        evalstring += 'xInteractions_xinteract_tmp.ctypes.data_as(c_void_p)'
        xInteractions_nXinteract_tmp = shape[0]
    if not (confidence is None):
        evalstring += ','
        evalstring += repr(IMSLS_CONFIDENCE)
        evalstring += ','
        evalstring += 'c_double(confidence)'
    if not (model is None):
        evalstring += ','
        evalstring += repr(IMSLS_MODEL)
        evalstring += ','
        # model = toNumpyArray(model, 'model', shape=shape, dtype='struct', expectedShape=(1))
        evalstring += 'byref(model)'
    if not (prederr is None):
        evalstring += ','
        evalstring += repr(IMSLS_PREDERR)
        checkForList(prederr, 'prederr')
        evalstring += ','
        prederr_prederr_tmp = c_double()
        evalstring += 'byref(prederr_prederr_tmp)'
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (prederr is None):
        processRet(prederr_prederr_tmp, shape=(1), pyvar=prederr)
    if confidence:
        if columnWise:
            return processRet(result, shape=(nClasses, 3, nObservations), result=True)
        else:
            return processRet(result, shape=(nObservations, nClasses, 3), result=True)
    else:
        if columnWise:
            return processRet(result, shape=(nClasses, nObservations), result=True)
        else:
            return processRet(result, shape=(nObservations, nClasses), result=True)
