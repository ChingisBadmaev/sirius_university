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
""" Structures for neural net routines
"""
from ctypes import POINTER, Structure, c_double, c_int

PI = POINTER(c_int)


class NnNode (Structure):
    _fields_ = [("layer_id", c_int),
                ("n_inLinks", c_int),
                ("n_outLinks", c_int),
                ("inLinks", PI),
                ("outLinks", PI),
                ("delta", c_double),
                ("bias", c_double),
                ("ActivationFcn", c_int)]


class NnLink (Structure):
    _fields_ = [("weight", c_double),
                ("to_node", c_int),
                ("from_node", c_int)]


class NnLayer (Structure):
    _fields_ = [("n_nodes", c_int),
                ("nodes", PI)]


class NnNetwork(Structure):
    _fields_ = [("n_layers", c_int),
                ("layers", POINTER(NnLayer)),
                ("n_links", c_int),
                ("next_link", PI),
                ("links", POINTER(NnLink)),
                ("n_nodes", c_int),
                ("nodes", POINTER(NnNode))]
