import unittest
from unittest.mock import patch, MagicMock
import types
import whisperWorkload  
import os
import logging
from whisperWorkload import setup_logger

class TestWhisper(unittest.TestCase):
    @patch('whisperWorkload.whisper.load_model')
    @patch('whisperWorkload.random.choice')
    def test_loadModel(self, mock_choice, mock_load_model):
        mock_choice.return_value = 'test.mp3' # Mocking return values

        # Mocking model object and its transcribe method
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {'test': 'result'}
        mock_load_model.return_value = mock_model

        # Call the function to test
        result, search_result = whisperWorkload.loadModel()

        # Assertions
        self.assertEqual(result, {'test': 'result'})

        self.assertIsInstance(result, dict) # result should be a dictionary
        self.assertIsInstance(search_result, types.GeneratorType) # search_result should be a list

        mock_load_model.side_effect = OSError("Test OSError") # Set up mock load_model to raise OSError

        with self.assertRaises(IOError): # Ensure that an IOError is handled gracefully
            whisperWorkload.loadModel() # Call loadModel with invalid file

        self.assertTrue(search_result) # search_result should not be empty  

    @patch('whisperWorkload.search')
    def test_performSearch(self, mock_search):
        # Mocking return value
        mock_search.return_value = ['result1', 'result2', 'result3', 'result4', 'result5']

        # Call the function to test
        result = whisperWorkload.performSearch('test query')

        # Assertions
        self.assertEqual(result, ['result1', 'result2', 'result3', 'result4', 'result5'])

    def test_findSoundFiles(self):
        # Mocking return value
        with patch('whisperWorkload.os.listdir') as mock_listdir:
            mock_listdir.return_value = ['test1.mp3', 'test2.mp3', 'test3.mp3']

            # Call the function to test
            result = whisperWorkload.findSoundFiles()

            # Assertions
            self.assertEqual(result, ['test1.mp3', 'test2.mp3', 'test3.mp3'])
    
    @patch('whisperWorkload.random.choice')
    def test_selectRandomFile(self, mock_choice):
        # Mocking return value
        mock_choice.return_value = 'test.mp3'

        # Call the function to test
        result = whisperWorkload.selectRandomFile(['test1.mp3', 'test2.mp3', 'test3.mp3'])

        # Assertions
        self.assertEqual(result, 'test.mp3')

        self.assertIsInstance(result, str) # result should be a string

    @patch('whisperWorkload.logging.getLogger')
    @patch('whisperWorkload.load_dotenv')
    @patch('whisperWorkload.logging_loki.LokiHandler')
    @patch('whisperWorkload.hostname', 'mock-hostname')
    @patch('whisperWorkload.workload_type', 'mock-workload')
    @patch('whisperWorkload.uuid', 'mock-uuid')
    def test_setup_logger(self, mock_LokiHandler, mock_load_dotenv, mock_getLogger):
        # Mock the environment variables
        mock_env = {
            'GRAFANACLOUD_URL': 'http://mock-url',
            'GRAFANACLOUD_USERNAME': 'mock-user',
            'GRAFANACLOUD_PASSWORD': 'mock-pass'
        }
        
        with patch.dict(os.environ, mock_env):
            # Mock the logger and its methods
            mock_logger = MagicMock()
            mock_getLogger.return_value = mock_logger

            # Mock the LokiHandler instance
            mock_handler = MagicMock()
            mock_LokiHandler.return_value = mock_handler

            # Call the setup_logger function
            setup_logger()

            # Check logger level is set to INFO
            mock_logger.setLevel.assert_called_with(logging.INFO)

            # Ensure load_dotenv was called
            mock_load_dotenv.assert_called_once()

            # Check if existing handlers were cleared
            mock_logger.handlers.clear.assert_called_once()

            # Check LokiHandler was created with correct parameters
            mock_LokiHandler.assert_called_once_with(
                url='http://mock-url',
                tags={
                    "application": "Workload",
                    "host": 'mock-hostname',
                    "workload":'mock-workload',
                    "affinity": "worker3",
                    "uuid": 'mock-uuid'
                },
                auth=('mock-user', 'mock-pass'),
                version="1"
            )

            # Check the handler was added to the logger
            mock_logger.addHandler.assert_called_once_with(mock_handler)

            # Verify formatter was set correctly
            mock_handler.setFormatter.assert_called_once()
            formatter_arg = mock_handler.setFormatter.call_args[0][0]
            self.assertIsInstance(formatter_arg, logging.Formatter)
            self.assertEqual(formatter_arg._fmt, '%(asctime)s - %(levelname)s - %(message)s')

    @patch('whisperWorkload.logging.getLogger')
    @patch('whisperWorkload.load_dotenv')
    @patch('whisperWorkload.logging_loki.LokiHandler', side_effect=Exception('mock error'))
    def test_setup_logger_exception(self, mock_LokiHandler, mock_load_dotenv, mock_getLogger):
        # Mock the environment variables
        mock_env = {
            'GRAFANACLOUD_URL': 'http://mock-url',
            'GRAFANACLOUD_USERNAME': 'mock-user',
            'GRAFANACLOUD_PASSWORD': 'mock-pass'
        }

        with patch.dict(os.environ, mock_env):
            # Mock the logger and its methods
            mock_logger = MagicMock()
            mock_getLogger.return_value = mock_logger

            # Expect the setup_logger to raise an exception
            with self.assertRaises(Exception) as context:
                setup_logger()

            self.assertEqual(str(context.exception), 'mock error')

if __name__ == '__main__':
    unittest.main()