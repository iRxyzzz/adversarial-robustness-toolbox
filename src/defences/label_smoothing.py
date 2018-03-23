from __future__ import absolute_import, division, print_function, unicode_literals

from src.defences.preprocessor import Preprocessor


class LabelSmoothing(Preprocessor):
    """
    Computes a vector of smooth labels from a vector of hard ones. The hard labels have to contain ones for the
    correct classes and zeros for all the others. The remaining probability mass between `max_value` and 1 is
    distributed uniformly between the incorrect classes for each instance.
    """
    params = ['max_value']

    def __init__(self, max_value=.9):
        """
        Create an instance of label smoothing.
        """
        self.is_fitted = True
        self.set_params(max_value=max_value)

    def __call__(self, x_val, y_val, max_value=0.9):
        """
        Apply label smoothing.

        :param x_val: (np.ndarray) Input data, will not be modified by this method
        :param y_val: (np.ndarray) Original vector of label probabilities (one-vs-rest)
        :param max_value: (float) Value to affect to correct label
        :return: (np.ndarray, np.ndarray) Unmodified input data and the vector of smooth probabilities as labels
        """
        self.set_params(max_value=max_value)

        min_value = (1 - max_value) / (y_val.shape[1] - 1)
        assert max_value >= min_value

        smooth_y = y_val.copy()
        smooth_y[smooth_y == 1.] = max_value
        smooth_y[smooth_y == 0.] = min_value
        return x_val, smooth_y

    def fit(self, x_val, y_val=None, **kwargs):
        """No parameters to learn for this method; do nothing."""
        pass

    def set_params(self, **kwargs):
        """Take in a dictionary of parameters and applies defense-specific checks before saving them as attributes.

        Defense-specific parameters:
        :param max_value: (float) Value to affect to correct label
        """
        # Save attack-specific parameters
        super(LabelSmoothing, self).set_params(**kwargs)

        if self.max_value <= 0 or self.max_value > 1:
            raise ValueError("The maximum value for correct labels must be between 0 and 1.")

        return True