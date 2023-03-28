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
from sys import platform


class d_complex (Structure):
    pass


d_complex._fields_ = [
    ('re', c_double),
    ('im', c_double)]


class f_complex (Structure):
    pass


f_complex._fields_ = [
    ('re', c_float),
    ('im', c_float)]


class tm(Structure):
    pass


if (platform == 'win32') or (platform == 'win64'):
    tm._fields_ = [
        ('tm_sec', c_int),
        ('tm_min', c_int),
        ('tm_hour', c_int),
        ('tm_mday', c_int),
        ('tm_mon', c_int),
        ('tm_year', c_int),
        ('tm_wday', c_int),
        ('tm_yday', c_int),
        ('tm_isdst', c_int)]
else:
    tm._fields_ = [
        ('tm_sec', c_int),
        ('tm_min', c_int),
        ('tm_hour', c_int),
        ('tm_mday', c_int),
        ('tm_mon', c_int),
        ('tm_year', c_int),
        ('tm_wday', c_int),
        ('tm_yday', c_int),
        ('tm_isdst', c_int),
        ('tm_getoff', c_long),
        ('tm_zone', c_char_p)]


class Imsl_d_ppoly (Structure):
    pass


Imsl_d_ppoly._fields_ = [
    ('domain_dim', c_int),
    ('target_dim', c_int),
    ('order', POINTER(c_int)),
    ('num_coef', POINTER(c_int)),
    ('num_breakpoints', POINTER(c_int)),
    ('breakpoints', POINTER(c_double)),
    ('coef', POINTER(c_double))]


class Imsl_d_spline (Structure):
    pass


Imsl_d_spline._fields_ = [
    ('domain_dim', c_int),
    ('target_dim', c_int),
    ('order', POINTER(c_int)),
    ('num_coef', POINTER(c_int)),
    ('num_knots', POINTER(c_int)),
    ('knots', POINTER(c_double)),
    ('coef', POINTER(c_double))]


class d_constraint_struct (Structure):
    pass


d_constraint_struct._fields_ = [
    ('xval', c_double),
    ('der', c_int),
    ('type', c_int),
    ('bl', c_double),
    ('bu', c_double)]


class Imsl_d_radial_basis_fit (Structure):
    pass


Imsl_d_radial_basis_fit._fields_ = [
    ('dimension', c_int),
    ('num_centers', c_int),
    ('additional_terms', c_int),
    ('centers', POINTER(c_double)),
    ('coefficients', POINTER(c_double)),
    ('radial_function', c_void_p),
    ('delta', c_double),
    ('fcn_2_data', c_void_p),
    ('fcn_2', c_void_p)]


class Imsl_d_sparse_elem (Structure):
    pass


Imsl_d_sparse_elem._fields_ = [
    ('row', c_int),
    ('col', c_int),
    ('val', c_double)]


class Imsl_c_sparse_elem (Structure):
    pass


Imsl_c_sparse_elem._fields_ = [
    ('row', c_int),
    ('col', c_int),
    ('val', d_complex)]


class Imsl_c_sparse_list_element_struct (Structure):
    pass


Imsl_c_sparse_list_element_struct._fields_ = [
    ('markowitz', c_int),
    ('ptr', c_void_p)]


class Imsl_c_header_element (Structure):
    pass


Imsl_c_header_element._fields_ = [
    ('markowitz', c_int),
    ('ptr', POINTER(Imsl_c_sparse_list_element_struct))]


class Imsl_d_sparse_list_element_struct (Structure):
    pass


Imsl_d_sparse_list_element_struct._fields_ = [
    ('val', c_double),
    ('i', c_int),
    ('j', c_int),
    ('next_row', POINTER(Imsl_d_sparse_list_element_struct)),
    ('next_col', POINTER(Imsl_d_sparse_list_element_struct))]


class Imsl_d_sparse_list_element_struct (Structure):
    pass


Imsl_d_sparse_list_element_struct._fields_ = [
    ('val', d_complex),
    ('i', c_int),
    ('j', c_int),
    ('next_row', POINTER(Imsl_c_sparse_list_element_struct)),
    ('prev_row', POINTER(Imsl_c_sparse_list_element_struct)),
    ('next_col', POINTER(Imsl_c_sparse_list_element_struct)),
    ('prev_col', POINTER(Imsl_c_sparse_list_element_struct))]


class Imsl_d_memory_list_struct (Structure):
    pass


Imsl_d_memory_list_struct._fields_ = [
    ('node', c_void_p),
    ('next', POINTER(Imsl_d_memory_list_struct))]


class Imsl_d_header_element (Structure):
    pass


Imsl_d_header_element._fields_ = [
    ('markowitz', c_int),
    ('ptr', POINTER(Imsl_d_sparse_list_element_struct))]


class Imsl_c_memory_list_struct (Structure):
    pass


Imsl_c_memory_list_struct._fields_ = [
    ('n', c_int),
    ('nz', c_int),
    ('row_pivots', POINTER(c_int)),
    ('col_pivots', POINTER(c_int)),
    ('row_ptr', POINTER(Imsl_d_header_element)),
    ('col_ptr', POINTER(Imsl_d_header_element))]


class Imsl_d_memory_list_struct (Structure):
    pass


Imsl_d_memory_list_struct._fields_ = [
    ('node', POINTER(Imsl_c_sparse_list_element_struct)),
    ('next', POINTER(Imsl_c_memory_list_struct))]


class Imsl_c_sparse_lu_factor (Structure):
    pass


Imsl_c_sparse_lu_factor._fields_ = [
    ('n', c_int),
    ('nz', c_int),
    ('row_pivots', POINTER(c_int)),
    ('col_pivots', POINTER(c_int)),
    ('row_ptr', POINTER(Imsl_c_header_element)),
    ('col_ptr', POINTER(Imsl_c_header_element))]


class Imsl_d_sparse_lu_factor (Structure):
    pass


Imsl_d_sparse_lu_factor._fields_ = [
    ('n', c_int),
    ('nz', c_int),
    ('row_pivots', POINTER(c_int)),
    ('col_pivots', POINTER(c_int)),
    ('row_ptr', POINTER(Imsl_c_header_element)),
    ('col_ptr', POINTER(Imsl_c_header_element))]


class Imsl_symbolic_factor (Structure):
    pass


Imsl_symbolic_factor._fields_ = [
    ('nzsub', POINTER(c_int)),
    ('xnzsub', POINTER(c_int)),
    ('maxsub', c_int),
    ('xlnz', POINTER(c_int)),
    ('maxlnz', c_int),
    ('perm', POINTER(c_int)),
    ('invp', POINTER(c_int)),
    ('multifrontal_space', c_int)]


class Imsl_d_numeric_factor (Structure):
    pass


Imsl_d_numeric_factor._fields_ = [
    ('nzsub', POINTER(c_int)),
    ('xnzsub', POINTER(c_int)),
    ('xlnz', POINTER(c_int)),
    ('alnz', POINTER(c_double)),
    ('perm', POINTER(c_int)),
    ('diag', POINTER(c_double))]


class Imsl_c_numeric_factor (Structure):
    pass


Imsl_c_numeric_factor._fields_ = [
    ('nzsub', POINTER(c_int)),
    ('xnzsub', POINTER(c_int)),
    ('xlnz', POINTER(c_int)),
    ('alnz', POINTER(d_complex)),
    ('perm', POINTER(c_int)),
    ('diag', POINTER(d_complex))]


class Imsl_faure (Structure):
    pass


Imsl_faure._fields_ = [
    ('nSkip', c_int),
    ('y', POINTER(c_int)),
    ('dim', c_int),
    ('maxDigits', c_int),
    ('base', c_int),
    ('digitsN', POINTER(c_int)),
    ('c', POINTER(c_int)),
    ('power', POINTER(c_int)),
    ('scale', c_double)]


class Imsl_d_mps (Structure):
    pass


Imsl_d_mps._fields_ = [
    ('filename', c_char_p),
    ('name', c_char * 9),
    ('nrows', c_int),
    ('ncolumns', c_int),
    ('nonzeros', c_int),
    ('nhessian', c_int),
    ('ninteger', c_int),
    ('nbinary', c_int),
    ('objective', POINTER(c_double)),
    ('constraint', POINTER(Imsl_d_sparse_elem)),
    ('hessian', POINTER(Imsl_d_sparse_elem)),
    ('lower_range', POINTER(c_double)),
    ('upper_range', POINTER(c_double)),
    ('lower_bound', POINTER(c_double)),
    ('upper_bound', POINTER(c_double)),
    ('variable_type', POINTER(c_int)),
    ('name_objective', c_char * 9),
    ('name_rhs', c_char * 9),
    ('name_ranges', c_char * 9),
    ('name_bounds', c_char * 9),
    ('name_row', POINTER(c_char_p)),
    ('name_column', POINTER(c_char_p)),
    ('positive_infinity', c_double),
    ('negative_infinity', c_double),
    ('objective_constant', c_double)]


class Imsl_d_hb_format (Structure):
    pass


Imsl_d_hb_format._fields_ = [
    ('nnz', c_int),
    ('nzval', POINTER(c_double)),
    ('rowind', POINTER(c_int)),
    ('colptr', POINTER(c_int))
]


class Imsl_c_hb_format (Structure):
    pass


Imsl_c_hb_format._fields_ = [
    ('nnz', c_int),
    ('nzval', POINTER(d_complex)),
    ('rowind', POINTER(c_int)),
    ('colptr', POINTER(c_int))
]


class Imsl_d_sc_format (Structure):
    pass


Imsl_d_sc_format._fields_ = [
    ('nnz', c_int),
    ('nsuper', c_int),
    ('nzval', POINTER(c_double)),
    ('nzval_colptr', POINTER(c_int)),
    ('rowind', POINTER(c_int)),
    ('rowind_colptr', POINTER(c_int)),
    ('col_to_sup', POINTER(c_int)),
    ('sup_to_col', POINTER(c_int))
]


class Imsl_c_sc_format (Structure):
    pass


Imsl_c_sc_format._fields_ = [
    ('nnz', c_int),
    ('nsuper', c_int),
    ('nzval', POINTER(d_complex)),
    ('nzval_colptr', POINTER(c_int)),
    ('rowind', POINTER(c_int)),
    ('rowind_colptr', POINTER(c_int)),
    ('col_to_sup', POINTER(c_int)),
    ('sup_to_col', POINTER(c_int))
]


class Imsl_d_super_lu_factor (Structure):
    pass


Imsl_d_super_lu_factor._fields_ = [
    ('nrow', c_int),
    ('ncol', c_int),
    ('equilibration_method', c_int),
    ('rowscale', POINTER(c_double)),
    ('columnscale ', POINTER(c_double)),
    ('rowperm', POINTER(c_int)),
    ('colperm', POINTER(c_int)),
    ('U', POINTER(Imsl_d_hb_format)),
    ('L', POINTER(Imsl_d_sc_format))
]


class Imsl_c_super_lu_factor (Structure):
    pass


Imsl_c_super_lu_factor._fields_ = [
    ('nrow', c_int),
    ('ncol', c_int),
    ('equilibration_method', c_int),
    ('rowscale', POINTER(c_double)),
    ('columnscale ', POINTER(c_double)),
    ('rowperm', POINTER(c_int)),
    ('colperm', POINTER(c_int)),
    ('U', POINTER(Imsl_c_hb_format)),
    ('L', POINTER(Imsl_c_sc_format))
]


class Imsl_d_hbp_format (Structure):
    pass


Imsl_d_hbp_format._fields_ = [
    ('nnz', c_int),
    ('nzval', POINTER(c_double)),
    ('rowind', POINTER(c_int)),
    ('colbeg', POINTER(c_int)),
    ('colend', POINTER(c_int)),
]


class Imsl_c_hbp_format (Structure):
    pass


Imsl_c_hbp_format._fields_ = [
    ('nnz', c_int),
    ('nzval', POINTER(d_complex)),
    ('rowind', POINTER(c_int)),
    ('colbeg', POINTER(c_int)),
    ('colend', POINTER(c_int)),
]


class Imsl_d_scp_format (Structure):
    pass


Imsl_d_scp_format._fields_ = [
    ('nnz', c_int),
    ('nsuper', c_int),
    ('nzval', POINTER(c_double)),
    ('nzval_colbeg', POINTER(c_int)),
    ('nzval_colend', POINTER(c_int)),
    ('rowind', POINTER(c_int)),
    ('rowind_colbeg', POINTER(c_int)),
    ('rowind_colend', POINTER(c_int)),
    ('col_to_sup', POINTER(c_int)),
    ('sup_to_colbeg', POINTER(c_int)),
    ('sup_to_colend', POINTER(c_int)),
]


class Imsl_c_scp_format (Structure):
    pass


Imsl_c_scp_format._fields_ = [
    ('nnz', c_int),
    ('nsuper', c_int),
    ('nzval', POINTER(d_complex)),
    ('nzval_colbeg', POINTER(c_int)),
    ('nzval_colend', POINTER(c_int)),
    ('rowind', POINTER(c_int)),
    ('rowind_colbeg', POINTER(c_int)),
    ('rowind_colend', POINTER(c_int)),
    ('col_to_sup', POINTER(c_int)),
    ('sup_to_colbeg', POINTER(c_int)),
    ('sup_to_colend', POINTER(c_int)),
]


class Imsl_d_super_lu_smp_factor (Structure):
    pass


Imsl_d_super_lu_smp_factor._fields_ = [
    ('nrow', c_int),
    ('ncol', c_int),
    ('equilibration_method', c_int),
    ('rowscale', POINTER(c_double)),
    ('columnscale', POINTER(c_double)),
    ('rowperm', POINTER(c_int)),
    ('colperm', POINTER(c_int)),
    ('U', POINTER(Imsl_d_hbp_format)),
    ('L', POINTER(Imsl_d_scp_format))]


class Imsl_c_super_lu_smp_factor (Structure):
    pass


Imsl_c_super_lu_smp_factor._fields_ = [
    ('nrow', c_int),
    ('ncol', c_int),
    ('equilibration_method', c_int),
    ('rowscale', POINTER(c_double)),
    ('columnscale', POINTER(c_double)),
    ('rowperm', POINTER(c_int)),
    ('colperm', POINTER(c_int)),
    ('U', POINTER(Imsl_c_hbp_format)),
    ('L', POINTER(Imsl_c_scp_format))]


class Imsl_snodal_symbolic_factor (Structure):
    pass


Imsl_snodal_symbolic_factor._fields_ = [
    ('nzsub', POINTER(POINTER(c_int))),
    ('xnzsub', POINTER(POINTER(c_int))),
    ('maxsub', c_int),
    ('xlnz', POINTER(POINTER(c_int))),
    ('maxlnz', c_int),
    ('perm', POINTER(POINTER(c_int))),
    ('invp', POINTER(POINTER(c_int))),
    ('multifrontal_space', c_int),
    ('nsuper', c_int),
    ('snode', POINTER(POINTER(c_int))),
    ('snode_ptr', POINTER(POINTER(c_int))),
    ('nleaves', c_int),
    ('etree_leaves', POINTER(POINTER(c_int)))]
