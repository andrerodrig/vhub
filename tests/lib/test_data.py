import pandas as pd
from django.test import TestCase

from vhub.lib.data import Data


class TestLibData(TestCase):
    
    columns=[
        "ASSET - HOSTNAME",
        "ASSET - IP_ADDRESS",
        "VULNERABILITY - TITLE",
        "VULNERABILITY - SEVERITY",
        "VULNERABILITY - CVSS",
        "VULNERABILITY - PUBLICATION_DATE"
    ]
    
    def _dummyfunc(**kwargs):
        """Helper function to test the argument passing in the method save_csv_data.
        """
        return kwargs
    
    def test_preprocess_none_values_raises_attribute_error(self):
        with self.assertRaises(AttributeError) as exc:
            _ = Data.preprocess_dataset(None)
            self.assertEqual(str(exc), "Processing failed. The dataset cannot be None.")
            
    def test_call_save_csv_data_with_filepath_none(self):
        with self.assertRaises(ValueError) as exc:
            Data.save_csv_data(None, self._dummyfunc)
            self.assertEqual(str(exc), "Failed to save. Invalid dataset file path.")
