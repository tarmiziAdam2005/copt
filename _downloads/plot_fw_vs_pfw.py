"""
Frank-Wolfe and Pairwise Frank-Wolfe
====================================

This example features a comparison in terms of convergence speed per iteration
between the Frank-Wolfe and the Pairwise Frank-Wolfe algorithms.
"""
import numpy as np
from scipy import sparse
import pylab as plt
import copt as cp

np.random.seed(0)

# .. generate some data ..
n_samples, n_features = 20, 20
#
# max_iter = 5000
# print('#features', n_features)
A = sparse.rand(n_samples, n_features, density=0.2)
ground_truth = np.random.randn(n_features)
b = A.dot(ground_truth) + np.random.randn(n_samples)

# make labels in {0, 1}
b = np.sign(b)
b = (b + 1) // 2
f = cp.utils.LogLoss(A, b)
alpha = 1./n_samples
L = cp.utils.get_lipschitz(A, f, alpha)

#
# # .. run the solver for different values ..
# # .. of the regularization parameter beta ..
all_betas = [1., 10., 100.]
all_trace_fw, all_trace_pfw = [], []
max_iter = [1000, 5000, 10000]
for i, beta in enumerate(all_betas):
    print('beta = %s' % beta)
    pen = cp.utils.L1Ball(beta)

    cb_fw = cp.utils.Trace(f)
    cp.minimize_FW(
        f.f_grad, pen.lmo, np.zeros(n_features), callback=cb_fw,
        max_iter=max_iter[i], verbose=True, tol=0)
    all_trace_fw.append(cb_fw.trace_fx)

    cb_pfw = cp.utils.Trace(f)
    cp.minimize_PFW_L1(
        f.f_grad, beta, n_features, callback=cb_pfw,
        max_iter=max_iter[i], verbose=True, tol=0, backtracking=True)
    all_trace_pfw.append(cb_pfw.trace_fx)


# .. plot the results ..
fig, ax = plt.subplots(1, 3, sharey=False)
xlim = [0.02, 0.02, 0.1]
for i, beta in enumerate(all_betas):

    fmin = min(np.min(all_trace_fw[i]), np.min(all_trace_pfw[i]))
    ax[i].plot(all_trace_fw[i] - fmin, label='FW')
    ax[i].plot(all_trace_pfw[i] - fmin, label='PFW')

    ax[i].set_xlabel('Iterations')
    ax[i].set_yscale('log')
    ax[i].set_ylim((1e-10, None))
    ax[i].grid(True)

plt.legend()
plt.show()