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

imslstat = loadimsl(STAT)


def kohonenSOMForecast(kohonen, data):
    """ Calculates forecasts using a trained Kohonen network.
    """
    imslstat.imsls_d_kohonenSOM_forecast.restype = POINTER(c_int)
    shape = []
    evalstring = 'imslstat.imsls_d_kohonenSOM_forecast('
    # kohonen = toNumpyArray(kohonen, 'kohonen', shape=shape, dtype='struct', expectedShape=(1))
    # evalstring +='kohonen.ctypes.data_as(c_void_p)'
    evalstring += 'kohonen'
    evalstring += ','
    evalstring += 'c_int(nobs)'
    evalstring += ','
    data = toNumpyArray(data, 'data', shape=shape,
                        dtype='double', expectedShape=(0, 0))
    evalstring += 'data.ctypes.data_as(c_void_p)'
    nobs = shape[0]
    dim = shape[1]
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(nobs, 2), result=True)
