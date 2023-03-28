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
from pyimsl.util.imslUtils import MATH, checkForBoolean, fatalErrorCheck, loadimsl, processRet
from numpy import shape
from ctypes import POINTER, c_double, c_int

IMSL_SYMMETRIC_STORAGE = 11094
imslmath = loadimsl(MATH)


def generateTestBand(n, c, symmetricStorage=None):
    """ Generates test matrices of class and E(n, c). Returns in band or band symmetric format.
    """
    imslmath.imsl_d_generate_test_band.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslmath.imsl_d_generate_test_band('
    evalstring += 'c_int(n)'
    evalstring += ','
    evalstring += 'c_int(c)'
    checkForBoolean(symmetricStorage, 'symmetricStorage')
    if (symmetricStorage):
        evalstring += ','
        evalstring += repr(IMSL_SYMMETRIC_STORAGE)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(MATH)
    if symmetricStorage:
        retshape = (c + 1, n)
    else:
        retshape = (2 * c + 1, n)
    return processRet(result, shape=retshape, result=True)
