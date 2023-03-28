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
from ctypes import *


class d_complex (Structure):
    pass


d_complex._fields_ = [
    ('re', c_double),
    ('im', c_double)]


class Imsls_d_ppoly (Structure):
    pass


Imsls_d_ppoly._fields_ = [
    ('domain_dim', c_int),
    ('target_dim', c_int),
    ('order', POINTER(c_int)),
    ('num_coef', POINTER(c_int)),
    ('num_breakpoints', POINTER(c_int)),
    ('breakpoints', POINTER(c_double)),
    ('coef', POINTER(c_double))]


class Imsls_d_survival (Structure):
    pass


Imsls_d_survival._fields_ = [
    ('nobs', c_int),
    ('ncol', c_int),
    ('model', c_int),
    ('ifix', c_int),
    ('intcep', c_int),
    ('nclvar', c_int),
    ('indcl', POINTER(c_int)),
    ('nef', c_int),
    ('nvef', POINTER(c_int)),
    ('indef', POINTER(c_int)),
    ('ncoef', c_int),
    ('nclval', POINTER(c_int)),
    ('clval', POINTER(c_double)),
    ('coef', POINTER(c_double))]


class Imsls_d_regression (Structure):
    pass


Imsls_d_regression._fields_ = [
    ('n_observations', c_int),
    ('n_cases_missing', c_int),
    ('n_dependent', c_int),
    ('n_parameters', c_int),
    ('intercept', c_int),
    ('rank', c_int),
    ('df_error', c_double),
    ('beta_hat', POINTER(c_double)),
    ('sscp_error', POINTER(c_double)),
    ('rxx_transpose', POINTER(c_double)),
    ('d', POINTER(c_double)),
    ('rxy_transpose', POINTER(c_double)),
    ('x_mean', POINTER(c_double)),
    ('x_minimum', POINTER(c_double)),
    ('x_maximum', POINTER(c_double)),
    ('y_mean', POINTER(c_double)),
    ('y_minimum', POINTER(c_double)),
    ('y_maximum', POINTER(c_double))]


class Imsls_d_arma (Structure):
    pass


Imsls_d_arma._fields_ = [
    ('a_variance', c_double),
    ('constant', c_double),
    ('z', POINTER(c_double)),
    ('ar', POINTER(c_double)),
    ('ma', POINTER(c_double)),
    ('ar_lags', POINTER(c_int)),
    ('ma_lags', POINTER(c_int)),
    ('n_observations', c_int),
    ('p', c_int),
    ('q', c_int),
    ('constant_option', c_int)]


class Imsls_d_poly_regression (Structure):
    pass


Imsls_d_poly_regression._fields_ = [
    ('x_minimum', c_double),
    ('x_maximum', c_double),
    ('y_minimum', c_double),
    ('y_maximum', c_double),
    ('dfe', c_double),
    ('sse', c_double),
    ('smultc', c_double),
    ('saddc', c_double),
    ('a', POINTER(c_double)),
    ('b', POINTER(c_double)),
    ('scoef', POINTER(c_double)),
    ('d', POINTER(c_double)),
    ('output_degree', c_int)]


class Imsls_faure (Structure):
    pass


Imsls_faure._fields_ = [
    ('nSkip', c_int),
    ('y', POINTER(c_int)),
    ('dim', c_int),
    ('maxDigits', c_int),
    ('base', c_int),
    ('digitsN', POINTER(c_int)),
    ('c', POINTER(c_int)),
    ('power', POINTER(c_int)),
    ('scale', c_double)]


class Imsls_d_NN_Node (Structure):
    pass


Imsls_d_NN_Node._fields_ = [
    ('layer_id', c_int),
    ('n_inLinks', c_int),
    ('n_outLinks', c_int),
    ('inLinks', POINTER(c_int)),
    ('outLinks', POINTER(c_int)),
    ('gradient', c_double),
    ('bias', c_double),
    ('ActivationFcn', c_int)]


class Imsls_NN_Layer (Structure):
    pass


Imsls_NN_Layer._fields_ = [
    ('n_nodes', c_int),
    ('nodes', POINTER(c_int))]


class Imsls_d_NN_Link (Structure):
    pass


Imsls_d_NN_Link._fields_ = [
    ('weight', c_double),
    ('gradient', c_double),
    ('to_node', c_int),
    ('from_node', c_int)]


class Imsls_d_NN_Network (Structure):
    pass


Imsls_d_NN_Network._fields_ = [
    ('n_layers', c_int),
    ('layers', POINTER(Imsls_NN_Layer)),
    ('n_links', c_int),
    ('next_link', c_int),
    ('links', POINTER(Imsls_d_NN_Link)),
    ('n_nodes', c_int),
    ('nodes', POINTER(Imsls_d_NN_Node))]
