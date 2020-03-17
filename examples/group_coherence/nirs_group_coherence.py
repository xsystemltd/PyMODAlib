#  PyMODAlib, a Python implementation of the algorithms from MODA (Multiscale Oscillatory Dynamics Analysis).
#  Copyright (C) 2020 Lancaster University
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
This is for testing the group coherence algorithm with known data.
The data are not supplied as part of PyMODAlib.
"""

import numpy as np
import scipy.io
from matplotlib import pyplot
from numpy import ndarray

from pymodalib.algorithms.group_coherence import dual_group_coherence

fs = 31.25

# 15 minutes.
sig_length = int(fs * 60 * 15)


def load_mat(filename: str) -> ndarray:
    cell = list(scipy.io.loadmat(filename).values())[3]

    out = np.empty((cell.shape[1], sig_length))

    for index in range(cell.shape[1]):
        out[index, :] = cell[0, index][0, :sig_length]

    return out


if __name__ == "__main__":
    import os

    os.environ["LD_LIBRARY_PATH"] = (
        "/usr/local/MATLAB/MATLAB_Runtime/v96/runtime/glnxa64:"
        "/usr/local/MATLAB/MATLAB_Runtime/v96/bin/glnxa64:"
        "/usr/local/MATLAB/MATLAB_Runtime/v96/sys/os/glnxa64:"
        "/usr/local/MATLAB/MATLAB_Runtime/v96/extern/bin/glnxa64"
    )

    times = np.arange(0, sig_length / fs, 1 / fs)

    group1_signals_a = load_mat("Cphd_O2satNIRS11.mat")
    group1_signals_b = load_mat("Cphd_Respiration_resampl.mat")
    group2_signals_a = load_mat("phd_O2satNIRS11.mat")
    group2_signals_b = load_mat("phd_Respiration_resampl.mat")

    freq, coh1, mean1, median1, std1, coh2, mean2, median2, std2 = dual_group_coherence(
        group1_signals_a, group1_signals_b, group2_signals_a, group2_signals_b, fs
    )

    pyplot.plot(freq, coh1)
    pyplot.plot(freq, mean1)

    pyplot.legend(["Mean coherence (group 1)", "Mean surrogates (group 1)"])

    pyplot.show()
