import os
from ctypes import cdll, POINTER, c_uint64, c_size_t, c_double

import amquery.utils.iof as iof
from amquery.core.distance.kmers_distr import SparseArray

jsdlib = None

# Jenson-Shanon divergence
def jsd(x, y):
    x = x.kmer_index
    y = y.kmer_index
    xcols_p = x.cols.ctypes.data_as(POINTER(c_uint64))
    xdata_p = x.data.ctypes.data_as(POINTER(c_double))
    ycols_p = y.cols.ctypes.data_as(POINTER(c_uint64))
    ydata_p = y.data.ctypes.data_as(POINTER(c_double))
    return jsdlib.jsd(xcols_p, xdata_p, len(x), ycols_p, ydata_p, len(y))

def weighted_unifrac():
    return 0

FFP_JSD = 'ffp-jsd'
WEIGHTED_UNIFRAC = 'weigthed-unifrac'
DEFAULT_DISTANCE = FFP_JSD
distances = {FFP_JSD: jsd, WEIGHTED_UNIFRAC: weighted_unifrac}


if __name__ == "__main__":
    raise RuntimeError()
else:
    libdir = os.path.dirname(os.path.abspath(__file__))
    jsdlib = cdll.LoadLibrary(iof.find_lib(libdir, "jsd"))
    jsdlib.jsd.argtypes = [POINTER(c_uint64), POINTER(c_double), c_size_t,
                           POINTER(c_uint64), POINTER(c_double), c_size_t]
    jsdlib.jsd.restype = c_double
