.. _unfolded:

Unfolded algorithms
===================

This package contains a collection of routines turning the optimization algorithms defined in :ref:`Optim <optim>`
into unfolded architectures.
Recall that optimization algorithms aim at solving problems of the form :math:`\datafid{x}{y} + \reg{x}`
where :math:`\datafid{\cdot}{\cdot}` is a data-fidelity term, :math:`\reg{\cdot}` is a regularization term.
The resulting fixed-point algorithms for solving these problems are of the form (see :ref:`Optim <optim>`)

.. math::

    \begin{aligned}
    z_{k+1} &= \operatorname{step}_f(x_k, z_k, y, A, ...)\\
    x_{k+1} &= \operatorname{step}_g(x_k, z_k, y, A, ...)
    \end{aligned}

where :math:`\operatorname{step}_f` and :math:`\operatorname{step}_g` are gradient and/or proximal steps on
:math:`f` and :math:`g` respectively.

Unfolded architectures (sometimes called 'unrolled architectures') are obtained by replacing parts of these algorithms
by learnable modules. In turn, they can be trained in an end-to-end fashion to solve inverse problems.

Unfolded
--------
The :class:`deepinv.unfolded.unfolded_builder` class is a generic class for building unfolded architectures. It provides
a trainable reconstruction network using a either pre-existing optimizer (e.g., "PGD") or
an iterator defined by the user. The user can choose which parameters (e.g., prior denoiser, step size, regularization
parameter, etc.) are learnable and which are not.

.. autosummary::
   :toctree: stubs
   :template: myfunc_template.rst
   :nosignatures:

   deepinv.unfolded.unfolded_builder

The builder depends on the backbone class for DEQs, :class:`deepinv.unfolded.BaseUnfold`.

.. autosummary::
   :toctree: stubs
   :template: myclass_template.rst
   :nosignatures:

   deepinv.unfolded.BaseUnfold


Deep Equilibrium
----------------
Deep Equilibrium models (DEQ) are a particular class of unfolded architectures where the backward pass
is performed via Fixed-Point iterations. DEQ algorithms can virtually unroll infinitely many layers leveraging
the **implicit function theorem**. The backward pass consists in looking for solutions of the fixed-point equation

.. math::

   v = \left(\frac{\partial \operatorname{FixedPoint}(x^\star)}{\partial x^\star} \right)^{\top} v + u.


where :math:`u` is the incoming gradient from the backward pass,
and :math:`x^\star` is the equilibrium point of the forward pass.

See `this tutorial <http://implicit-layers-tutorial.org/deep_equilibrium_models/>`_ for more details.

The :class:`deepinv.unfolded.DEQ_builder` class is a generic class for building Deep Equilibrium (DEQ) architectures.

.. autosummary::
   :toctree: stubs
   :template: myfunc_template.rst
   :nosignatures:

    deepinv.unfolded.DEQ_builder

The builder depends on the backbone class for DEQs, :class:`deepinv.unfolded.BaseDEQ`.

.. autosummary::
   :toctree: stubs
   :template: myclass_template.rst
   :nosignatures:

    deepinv.unfolded.BaseDEQ