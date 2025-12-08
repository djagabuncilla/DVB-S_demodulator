import unittest
import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from functions.functions import fast_fourier_transform, inverse_fast_fourier_transform

class Test_Functions(unittest.TestCase):
    def test_FFT_IFFT(self):
        signal = [1.0 + 0j, 2.0 + 1j, 3.0 - 1j, 4.0 + 2j, 5.0 + 3j]

        spectrum = fast_fourier_transform(signal)
        editet_signal = inverse_fast_fourier_transform(spectrum)

        #self.assertEqual(len(editet_signal), len(signal)) 

        for i in range(len(signal)):

            self.assertAlmostEqual(editet_signal[i].real, 
                                   signal[i].real, 
                                   places=10,
                                   msg=f"В действительной части сигнал расходится на отсчёте {i}"
                                   )
            self.assertAlmostEqual(editet_signal[i].imag, 
                                   signal[i].imag, 
                                   places=10,
                                   msg=f"В мнимой части сигнал расходится на отсчёте {i}"
                                   )
            
if __name__ == '__main__':
    unittest.main()