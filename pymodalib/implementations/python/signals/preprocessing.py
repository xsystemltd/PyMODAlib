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
import numpy as np
from numpy import ndarray


def preprocess_impl(sig: ndarray, fs: float, fmin: float, fmax: float) -> ndarray:
    try:
        x, y = sig.shape
        if y > x:
            sig = sig.reshape(y)
    except ValueError:
        pass

    if fmin is None:
        fmin = 0
    if fmax is None:
        fmax = fs / 2

    L = len(sig)

    # De-trending.
    X = np.arange(1, len(sig) + 1).T / fs
    XM = np.ones((len(X), 4))

    for pn in range(1, 4):
        CX = X ** pn
        XM[:, pn] = (CX - np.mean(CX)) / np.std(CX)

    sig = sig.reshape(len(sig), 1)
    new_sig = sig - XM @ ((np.linalg.pinv(XM)) @ sig)

    # Filtering.
    fx = np.fft.fft(new_sig, axis=0)
    Nq = np.int32(np.ceil((L + 1) / 2))

    ff = np.concatenate([np.arange(0, Nq), -np.flip(np.arange(1, L - Nq + 1))]) * fs / L
    ff = ff.reshape(len(ff), 1)

    abs_ff = np.abs(ff)

    fx[(abs_ff <= np.max([fmin, fs / L])) | (abs_ff >= fmax)] = 0

    result = np.real(np.fft.ifft(fx, axis=0))

    try:
        x, y = result.shape
        if y == 1:
            result = result.reshape(x)
    except ValueError:
        pass

    return result
