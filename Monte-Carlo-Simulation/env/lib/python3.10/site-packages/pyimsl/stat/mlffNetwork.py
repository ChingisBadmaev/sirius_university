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
from pyimsl.util.imslUtils import STAT, checkForBoolean, checkForList, checkForDict, fatalErrorCheck, loadimsl, toNumpyArray
from pyimsl.util.VersionFacade import VersionFacade
from numpy import double, dtype, int, shape, size
from ctypes import byref, c_int, c_void_p
from .statStructs import Imsls_d_NN_Network

IMSLS_CREATE_HIDDEN_LAYER = 40600
IMSLS_ACTIVATION_FCN = 40601
IMSLS_BIAS = 40602
IMSLS_LINK_ALL = 40603
IMSLS_LINK_LAYER = 40605
IMSLS_LINK_NODE = 40604
IMSLS_REMOVE_LINK = 40606
IMSLS_WEIGHTS = 15400
IMSLS_N_LINKS = 40607
IMSLS_DISPLAY_NETWORK = 40608

LINEAR = 0
LOGISTIC = 1
TANH = 2
SQUASH = 3

imslstat = loadimsl(STAT)


def mlffNetwork(network, createHiddenLayer=None, activationFcn=None, bias=None, linkAll=None, linkLayer=None, linkNode=None, removeLink=None, weights=None, nLinks=None, displayNetwork=None):
    """ Creates a multilayered feedforward neural network.
    """
    VersionFacade.checkVersion(6)
    imslstat.imsls_d_mlff_network.restype = None
    shape = []
    evalstring = 'imslstat.imsls_d_mlff_network('
    evalstring += 'network'
    if not (createHiddenLayer is None):
        evalstring += ','
        evalstring += repr(IMSLS_CREATE_HIDDEN_LAYER)
        evalstring += ','
        evalstring += 'c_int(createHiddenLayer)'
    if not (activationFcn is None):
        evalstring += ','
        evalstring += repr(IMSLS_ACTIVATION_FCN)
        checkForDict(activationFcn, 'activationFcn',
                     ['layerId', 'activationFcn'])
        evalstring += ','
        activationFcn_layerId_tmp = activationFcn['layerId']
        evalstring += 'c_int(activationFcn_layerId_tmp)'
        evalstring += ','
        activationFcn_activationFcn_tmp = activationFcn['activationFcn']
        activationFcn_activationFcn_tmp = toNumpyArray(
            activationFcn_activationFcn_tmp, 'activationFcn', shape=shape, dtype='int')
        evalstring += 'activationFcn_activationFcn_tmp.ctypes.data_as(c_void_p)'
    if not (bias is None):
        evalstring += ','
        evalstring += repr(IMSLS_BIAS)
        checkForDict(bias, 'bias', ['layerId', 'bias'])
        evalstring += ','
        bias_layerId_tmp = bias['layerId']
        evalstring += 'c_int(bias_layerId_tmp)'
        evalstring += ','
        bias_bias_tmp = bias['bias']
        bias_bias_tmp = toNumpyArray(
            bias_bias_tmp, 'bias', shape=shape, dtype='double')
        evalstring += 'bias_bias_tmp.ctypes.data_as(c_void_p)'
    checkForBoolean(linkAll, 'linkAll')
    if (linkAll):
        evalstring += ','
        evalstring += repr(IMSLS_LINK_ALL)
    if not (linkLayer is None):
        evalstring += ','
        evalstring += repr(IMSLS_LINK_LAYER)
        checkForDict(linkLayer, 'linkLayer', ['to', 'from'])
        evalstring += ','
        linkLayer_to_tmp = linkLayer['to']
        evalstring += 'c_int(linkLayer_to_tmp)'
        evalstring += ','
        linkLayer_t_from_tmp = linkLayer['from']
        evalstring += 'c_int(linkLayer_t_from_tmp)'
    if not (linkNode is None):
        evalstring += ','
        evalstring += repr(IMSLS_LINK_NODE)
        checkForDict(linkNode, 'linkNode', ['to', 'from'])
        evalstring += ','
        linkNode_to_tmp = linkNode['to']
        evalstring += 'c_int(linkNode_to_tmp)'
        evalstring += ','
        linkNode_t_from_tmp = linkNode['from']
        evalstring += 'c_int(linkNode_t_from_tmp)'
    if not (removeLink is None):
        evalstring += ','
        evalstring += repr(IMSLS_REMOVE_LINK)
        checkForDict(removeLink, 'removeLink', ['to', 'from'])
        evalstring += ','
        removeLink_to_tmp = removeLink['to']
        evalstring += 'c_int(removeLink_to_tmp)'
        evalstring += ','
        removeLink_t_from_tmp = removeLink['from']
        evalstring += 'c_int(removeLink_t_from_tmp)'
    if not (weights is None):
        evalstring += ','
        evalstring += repr(IMSLS_WEIGHTS)
        evalstring += ','
        weights = toNumpyArray(weights, 'weights', shape=shape, dtype='double')
        evalstring += 'weights.ctypes.data_as(c_void_p)'
    if not (nLinks is None):
        evalstring += ','
        evalstring += repr(IMSLS_N_LINKS)
        checkForList(nLinks, 'nLinks')
        evalstring += ','
        nLinks_nLinks_tmp = c_int()
        evalstring += 'byref(nLinks_nLinks_tmp)'
    if not (displayNetwork is None):
        VersionFacade.checkVersion(7)
        evalstring += ','
        evalstring += repr(IMSLS_DISPLAY_NETWORK)
    evalstring += ', 0)'
    result = eval(evalstring)
    fatalErrorCheck(STAT)
    if not (nLinks is None):
        processRet(nLinks_nLinks_tmp, shape=1, pyvar=nLinks)
    return
