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
    ('n_inputs', c_int),
    ('n_outputs', c_int),
    ('n_layers', c_int),
    ('layers', POINTER(Imsls_NN_Layer)),
    ('n_links', c_int),
    ('next_link', c_int),
    ('links', POINTER(Imsls_d_NN_Link)),
    ('n_nodes', c_int),
    ('nodes', POINTER(Imsls_d_NN_Node))]


class Imsls_d_chromosome (Structure):
    pass


Imsls_d_chromosome._fields_ = [
    ('binaryIndex', c_int),
    ('nominalIndex', c_int),
    ('integerIndex', c_int),
    ('realIndex', c_int),
    ('c_length', c_int),
    ('total_length', c_int),
    ('n_binary', c_int),
    ('n_nominal', c_int),
    ('n_integer', c_int),
    ('n_intBits', c_int),
    ('n_real', c_int),
    ('n_realBits', c_int),
    ('n_categories', POINTER(c_int)),
    ('i_intervals', POINTER(c_int)),
    ('i_bits', POINTER(c_int)),
    ('i_bounds', POINTER(c_int)),
    ('r_intervals', POINTER(c_int)),
    ('r_bits', POINTER(c_int)),
    ('allele', POINTER(c_int)),
    ('r_bounds', POINTER(c_double))]


class Imsls_d_individual (Structure):
    pass


Imsls_d_individual._fields_ = [
    ('n_parents', c_int),
    ('encoding', c_int),
    ('total_length', c_int),
    ('chromosome', POINTER(Imsls_d_chromosome)),
    ('parent', POINTER(c_int)),
    ('nominalPhenotype', POINTER(c_int)),
    ('binaryPhenotype', POINTER(c_int)),
    ('integerPhenotype', POINTER(c_int)),
    ('realPhenotype', POINTER(c_double))]


class Imsls_d_population (Structure):
    pass


Imsls_d_population._fields_ = [
    ('n', c_int),
    ('indexFittest', c_int),
    ('indexWeakest', c_int),
    ('avgFitness', c_double),
    ('stdFitness', c_double),
    ('maxFitness', c_double),
    ('minFitness', c_double),
    ('fitness', POINTER(c_double)),
    ('chromosome', POINTER(Imsls_d_chromosome)),
    ('individual', POINTER(POINTER(Imsls_d_individual)))]


class Imsls_d_nb_classifier (Structure):
    pass


Imsls_d_nb_classifier._fields_ = [
    ('avg', POINTER(c_double)),
    ('s', POINTER(c_double)),
    ('logMeans', POINTER(c_double)),
    ('logStdev', POINTER(c_double)),
    ('a', POINTER(c_double)),
    ('b', POINTER(c_double)),
    ('theta', POINTER(c_double)),
    ('class_pdf', POINTER(c_double)),
    ('conditional_nominal_pdf', POINTER(c_double)),
    ('i_pdf', POINTER(c_int)),
    ('n_categories', POINTER(c_int)),
    ('n_classes', c_int),
    ('n_nominal', c_int),
    ('n_continuous', c_int),
    ('dlambda', c_double),
    ('clambda', c_double),
    ('zero_correction', c_double)]


class Imsls_d_svm_node (Structure):
    pass


Imsls_d_svm_node._fields_ = [
    ('index', c_int),
    ('value', c_double)]


class Imsls_d_svm_parameter (Structure):
    pass


Imsls_d_svm_parameter._fields_ = [
    ('svm_type', c_int),
    ('kernel_type', c_int),
    ('n_attributes', c_int),
    ('n_patterns_precomputed', c_int),
    ('degree', c_int),
    ('gamma', c_double),
    ('coef0', c_double),
    ('cache_size', c_double),
    ('eps', c_double),
    ('C', c_double),
    ('nr_weight', c_int),
    ('weight_class', POINTER(c_double)),
    ('weight', POINTER(c_double)),
    ('nu', c_double),
    ('p', c_double),
    ('shrinking', c_int),
    ('probability', c_int)]


class Imsls_d_svm_model (Structure):
    pass


Imsls_d_svm_model._fields_ = [
    ('param', POINTER(Imsls_d_svm_parameter)),
    ('nr_class', c_int),
    ('n_attributes', c_int),
    ('l', c_int),
    ('SV', POINTER(POINTER(Imsls_d_svm_node))),
    ('sv_length', c_int),
    ('sv_coef_length', c_int),
    ('sv_coef', POINTER(c_double)),
    ('rho', POINTER(c_double)),
    ('probA', POINTER(c_double)),
    ('probB', POINTER(c_double)),
    ('label', POINTER(c_double)),
    ('nSV', POINTER(c_int)),
    ('free_sv', c_int)]


class Imsls_d_model (Structure):
    pass


Imsls_d_model._fields_ = [
    ('n_obs', c_int),
    ('n_updates', c_int),
    ('n_coefs', c_int),
    ('loglike', c_double),
    ('meany', POINTER(c_double)),
    ('coefs', POINTER(c_double)),
    ('stderrs', POINTER(c_double)),
    ('hess', POINTER(c_double)),
    ('grad', POINTER(c_double))]


class Imsls_apriori_items (Structure):
    pass


Imsls_apriori_items._fields_ = [
    ('n_items', c_int),
    ('items', POINTER(c_int)),
    ('support', c_int)]


class Imsls_d_apriori_itemsets (Structure):
    pass


Imsls_d_apriori_itemsets._fields_ = [
    ('n_itemsets', c_int),
    ('itemsets', POINTER(Imsls_apriori_items)),
    ('n_trans', c_int),
    ('max_num_products', c_int),
    ('max_set_size', c_int),
    ('min_pct_support', c_double)]


class Imsls_d_rule_components (Structure):
    pass


Imsls_d_rule_components._fields_ = [
    ('n_x', c_int),
    ('x', POINTER(c_int)),
    ('n_y', c_int),
    ('y', POINTER(c_int)),
    ('support', POINTER(c_int)),
    ('confidence', c_double),
    ('lift', c_double)]


class Imsls_d_association_rules (Structure):
    pass


Imsls_d_association_rules._fields_ = [
    ('n_rules', c_int),
    ('rules', POINTER(Imsls_d_rule_components))]


class Imsls_d_kohonenSOM (Structure):
    pass


Imsls_d_kohonenSOM._fields_ = [
    ('grid', c_int),
    ('type', c_int),
    ('wrap', c_int),
    ('dim', c_int),
    ('nrow', c_int),
    ('ncol', c_int),
    ('weights', POINTER(c_double))]


class Imsls_d_tree_node (Structure):
    pass


Imsls_d_tree_node._fields_ = [
    ('node_id', c_int),
    ('parent_id', c_int),
    ('node_var_id', c_int),
    ('n_children', c_int),
    ('children_ids', POINTER(c_int)),
    ('node_values_ind', POINTER(c_int)),
    ('node_prob', POINTER(c_double)),
    ('cost', c_double),
    ('y_probs', POINTER(c_double)),
    ('predicted_val', c_double),
    ('n_cases', c_double),
    ('surrogate_info', POINTER(c_double)),
    ('predicted_class', c_int),
    ('node_split_value', c_double)]


class Imsls_d_decision_tree (Structure):
    pass


Imsls_d_decision_tree._fields_ = [
    ('n_levels', c_int),
    ('n_nodes', c_int),
    ('response_type', c_int),
    ('pred_type', POINTER(c_int)),
    ('pred_n_values', POINTER(c_int)),
    ('n_classes', c_int),
    ('n_preds', c_int),
    ('n_surrogates', c_int),
    ('terminal_nodes', POINTER(c_int)),
    ('nodes', POINTER(Imsls_d_tree_node))]
