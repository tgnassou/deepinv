from deepinv.physics.forward import DecomposablePhysics
import torch


class Inpainting(DecomposablePhysics):
    r"""

    Inpainting forward operator, keeps a subset of entries.

    The operator is described by the diagonal matrix

    .. math::

        A = \text{diag}(m) \in \mathbb{R}^{n\times n}

    where :math:`m` is a binary mask with n entries.

    This operator is linear and has a trivial SVD decomposition, which allows for fast computation
    of the pseudo-inverse and proximal operator.

    An existing operator can be loaded from a saved ``.pth`` file via ``self.load_state_dict(save_path)``,
    in a similar fashion to ``torch.nn.Module``.

    :param tuple tensor_size: size of the input images, e.g., (C, H, W).
    :param torch.tensor, float mask: If the input is a float, the entries of the mask will be sampled from a bernoulli
        distribution with probability equal to ``mask``. If the input is a ``torch.tensor`` matching tensor_size,
        the mask will be set to this tensor.
    :param torch.device device: gpu or cpu
    :param bool pixelwise: Apply the mask in a pixelwise fashion, i.e., zero all channels in a given pixel simultaneously.

    |sep|

    :Examples:

        Inpainting operator using defined mask, removing the second column of a 3x3 image:

        >>> seed = torch.manual_seed(0) # Random seed for reproducibility
        >>> x = torch.randn(1, 1, 3, 3) # Define random 3x3 image
        >>> m = torch.zeros(1, 3, 3) # Define empty mask
        >>> m[:, 2, :] = 1 # Keeping last line only
        >>> physics = Inpainting(tensor_size=(1, 1, 3, 3), mask=m)
        >>> physics(x)
        tensor([[[[ 0.0000, -0.0000, -0.0000],
                  [ 0.0000, -0.0000, -0.0000],
                  [ 0.4033,  0.8380, -0.7193]]]])

        Inpainting operator using random mask, keeping 70% of the entries of a 3x3 image:

        >>> seed = torch.manual_seed(0) # Random seed for reproducibility
        >>> x = torch.randn(1, 3, 3) # Define random 3x3 image
        >>> physics = Inpainting(tensor_size=(1, 1, 3, 3), mask=0.7)
        >>> physics(x)
        tensor([[[[[ 1.5410, -0.0000, -2.1788],
                   [ 0.0000, -1.0845, -1.3986],
                   [ 0.0000,  0.8380, -0.7193]]]]])

    """

    def __init__(self, tensor_size, mask=0.3, pixelwise=True, device="cpu", **kwargs):
        super().__init__(**kwargs)
        self.tensor_size = tensor_size

        if isinstance(mask, torch.Tensor):  # check if the user created mask
            self.mask = mask
        else:  # otherwise create new random mask
            mask_rate = mask
            self.mask = torch.ones(tensor_size, device=device)
            aux = torch.rand_like(self.mask)
            if not pixelwise:
                self.mask[aux > mask_rate] = 0
            else:
                self.mask[:, aux[0, :, :] > mask_rate] = 0

        self.mask = torch.nn.Parameter(self.mask.unsqueeze(0), requires_grad=False)

    def noise(self, x):
        r"""
        Incorporates noise into the measurements :math:`\tilde{y} = N(y)`

        :param torch.Tensor x:  clean measurements
        :return torch.Tensor: noisy measurements
        """
        noise = self.U(
            self.V_adjoint(self.V(self.U_adjoint(self.noise_model(x)) * self.mask))
        )
        return noise
