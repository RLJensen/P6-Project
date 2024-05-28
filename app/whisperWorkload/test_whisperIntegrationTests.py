import unittest
from unittest.mock import patch, MagicMock
import whisperWorkload
import logging
import pytest
from whisperWorkload import startWorkload

class TestWhisperIntegrationNoLogging(unittest.TestCase):
    @patch('whisperWorkload.performSearch')
    @patch('whisperWorkload.whisper.load_model')
    @patch('whisperWorkload.os.listdir')
    @patch('whisperWorkload.random.choice')
    def test_start_workload_integration(self, mock_choice, mock_listdir, mock_load_model, mock_perform_search):
        """Integration test to verify complete workload execution."""
        # Mock the directory listing to contain MP3 files
        mock_listdir.return_value = ['test1.mp3', 'test2.mp3']
        mock_choice.return_value = 'test1.mp3'

        # Mock the whisper model's transcribe method
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {'transcription': 'test transcription'}
        mock_load_model.return_value = mock_model

        # Mock the search function to return some results
        mock_perform_search.return_value = ['result1', 'result2']

        # Run the workload function
        result, search_results = whisperWorkload.loadModel()

        # Verify that the transcription result and search results are correct
        self.assertEqual(result, {'transcription': 'test transcription'})
        self.assertEqual(search_results, ['result1', 'result2'])

    @patch('whisperWorkload.search')
    def test_perform_search(self, mock_search):
        """Integration test to ensure search function returns proper results."""
        mock_search.return_value = ['result1', 'result2', 'result3']

        results = whisperWorkload.performSearch('sample query')

        self.assertEqual(results, ['result1', 'result2', 'result3'])
    
    @patch('whisperWorkload.os.listdir')
    def test_load_model_no_sound_files(self, mock_listdir):
        """Integration test to ensure FileNotFoundError is raised when no sound files are found."""
        # Mock an empty directory (no MP3 files)
        mock_listdir.return_value = []

        # Attempt to call loadModel and expect a FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            whisperWorkload.loadModel()

# Custom logging handler to capture log outputs for verification
class LogCapture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)

@pytest.fixture
def log_capture():
    log_capture = LogCapture()
    logging.getLogger().addHandler(log_capture)
    yield log_capture
    logging.getLogger().removeHandler(log_capture)

def test_startWorkload(log_capture, capsys):
    with patch('whisperWorkload.loadModel') as mock_loadModel:
        # Setup the return value of loadModel mock
        mock_loadModel.return_value = (
            {"key1": "value1", "key2": "value2"},
            ["info1", "info2"]
        )

        startWorkload()

        # Verify the print output
        captured = capsys.readouterr()
        assert "key1 : value1" in captured.out
        assert "key2 : value2" in captured.out



if __name__ == '__main__':
    unittest.main()