import nibabel as nib
import numpy as np


def save_nii(nii, affine, header, file):
    nii = nii.astype(np.uint16)
    nib.save(nib.Nifti1Image(nii, affine=affine, header=header), file)