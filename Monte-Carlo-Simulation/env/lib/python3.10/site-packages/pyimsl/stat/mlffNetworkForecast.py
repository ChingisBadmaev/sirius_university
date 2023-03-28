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
from pyimsl.util.imslUtils import STAT, fatalErrorCheck, loadimsl, processRet, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, int, shape
from ctypes import POINTER, c_double, c_int, c_void_p
from .statStructs import Imsls_d_NN_Network

imslstat = loadimsl(STAT)


def mlffNetworkForecast(network, nominal, continuous):
    """ Calculates forecasts for trained multilayered feedforward neural networks.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_mlff_network_forecast.restype = POINTER(c_double)
    shape = []
    evalstring = 'imslstat.imsls_d_mlff_network_forecast('
    evalstring += 'network'
    evalstring += ','
    evalstring += 'c_int(nNominal)'
    evalstring += ','
    evalstring += 'c_int(nContinuous)'
    evalstring += ','
    nominal = toNumpyArray(nominal, 'nominal', shape=shape,
                           dtype='int', expectedShape=(0))
    evalstring += 'nominal.ctypes.data_as(c_void_p)'
    nNominal = shape[0]
    evalstring += ','
    continuous = toNumpyArray(continuous, 'continuous',
                              shape=shape, dtype='double', expectedShape=(0))
    evalstring += 'continuous.ctypes.data_as(c_void_p)'
    nContinuous = shape[0]
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    return processRet(result, shape=(network[0].layers[network[0].n_layers - 1].n_nodes), result=True)
