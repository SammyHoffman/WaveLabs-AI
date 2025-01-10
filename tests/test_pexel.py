# # tests/test_pexel.py

# import unittest
# from unittest.mock import patch, mock_open
# import os
# import requests  # Ensure requests is imported
# from modules.download.download_pexel import (
#     download_photo,
#     read_downloaded_photo_ids,
#     write_downloaded_photo_ids,
#     search_and_download_photos
# )

# class TestDownloadPexel(unittest.TestCase):
#     @patch('modules.download.download_pexel.requests.get')
#     @patch('modules.download.download_pexel.os.makedirs')
#     def test_download_photo_success(self, mock_makedirs, mock_get):
#         # Mock successful response
#         mock_response = unittest.mock.Mock()
#         mock_response.status_code = 200
#         mock_response.iter_content = lambda chunk_size: [b'test data']
#         mock_get.return_value = mock_response

#         with patch('builtins.open', mock_open()) as mocked_file:
#             download_photo('http://example.com/photo.jpg', '/fake/folder', '123456')
#             mock_makedirs.assert_called_with('/fake/folder', exist_ok=True)
#             mocked_file.assert_called_with('/fake/folder/123456.jpg', 'wb')
#             handle = mocked_file()
#             handle.write.assert_called_with(b'test data')

#     @patch('modules.download.download_pexel.requests.get')
#     @patch('modules.download.download_pexel.os.makedirs')
#     def test_download_photo_failure(self, mock_makedirs, mock_get):
#         # Mock failed response
#         mock_response = unittest.mock.Mock()
#         mock_response.status_code = 404
#         mock_get.return_value = mock_response

#         with patch('builtins.print') as mocked_print:
#             download_photo('http://example.com/photo.jpg', '/fake/folder', '123456')
#             mock_makedirs.assert_called_with('/fake/folder', exist_ok=True)
#             mocked_print.assert_called_with('Failed to download photo 123456 | Status Code: 404')

#     @patch('modules.download.download_pexel.requests.get', side_effect=requests.exceptions.RequestException)
#     @patch('modules.download.download_pexel.os.makedirs')
#     def test_download_photo_exception(self, mock_makedirs, mock_get):
#         with patch('builtins.print') as mocked_print:
#             download_photo('http://example.com/photo.jpg', '/fake/folder', '123456')
#             mock_makedirs.assert_called_with('/fake/folder', exist_ok=True)
#             mocked_print.assert_called_with('Exception occurred while downloading photo 123456: ')

#     def test_read_downloaded_photo_ids_existing_file(self):
#         mock_file_data = "123456\n234567\n345678\n"
#         with patch('modules.download.download_pexel.os.path.exists', return_value=True):
#             with patch('builtins.open', mock_open(read_data=mock_file_data)):
#                 result = read_downloaded_photo_ids('content/downloaded_pexel_photos.txt')
#                 self.assertEqual(result, {'123456', '234567', '345678'})

#     def test_read_downloaded_photo_ids_empty_file(self):
#         with patch('modules.download.download_pexel.os.path.exists', return_value=True):
#             with patch('builtins.open', mock_open(read_data='')):
#                 result = read_downloaded_photo_ids('content/downloaded_pexel_photos.txt')
#                 self.assertEqual(result, set())

#     def test_read_downloaded_photo_ids_nonexistent_file(self):
#         with patch('modules.download.download_pexel.os.path.exists', return_value=False):
#             result = read_downloaded_photo_ids('content/downloaded_pexel_photos.txt')
#             self.assertEqual(result, set())

#     @patch('modules.download.download_pexel.os.makedirs')
#     def test_write_downloaded_photo_ids_success(self, mock_makedirs):
#         with patch('builtins.open', mock_open()) as mocked_file:
#             write_downloaded_photo_ids('content/downloaded_pexel_photos.txt', {'123456', '234567'})
#             mock_makedirs.assert_called_with('content', exist_ok=True)
#             mocked_file.assert_called_with('content/downloaded_pexel_photos.txt', 'a')
#             handle = mocked_file()
#             handle.write.assert_any_call('123456\n')
#             handle.write.assert_any_call('234567\n')

#     @patch('modules.download.download_pexel.os.makedirs', side_effect=Exception('Permission denied'))
#     def test_write_downloaded_photo_ids_exception(self, mock_makedirs):
#         with patch('builtins.print') as mocked_print:
#             write_downloaded_photo_ids('content/downloaded_pexel_photos.txt', {'123456'})
#             mocked_print.assert_called_with('Exception occurred while writing to log file content/downloaded_pexel_photos.txt: Permission denied')

#     @patch('modules.download.download_pxel.requests.get')
#     @patch('modules.download.download_pxel.download_photo')
#     def test_search_and_download_photos_success(self, mock_download_photo, mock_get):
#         # Mock API response
#         mock_response = unittest.mock.Mock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             'photos': [
#                 {'id': 123456, 'src': {'original': 'http://example.com/photo1.jpg'}},
#                 {'id': 234567, 'src': {'original': 'http://example.com/photo2.jpg'}}
#             ]
#         }
#         mock_get.return_value = mock_response

#         with patch('modules.download.download_pexel.read_downloaded_photo_ids', return_value=set()):
#             search_and_download_photos(['nature'], total_photos=2, folder='/fake/folder', log_file='content/downloaded_pexel_photos.txt')
#             mock_download_photo.assert_any_call('http://example.com/photo1.jpg', '/fake/folder', '123456')
#             mock_download_photo.assert_any_call('http://example.com/photo2.jpg', '/fake/folder', '234567')

#     @patch('modules.download.download_pexel.requests.get', return_value=unittest.mock.Mock(status_code=429))
#     @patch('modules.download.download_pexel.time.sleep')
#     def test_search_and_download_photos_rate_limit(self, mock_sleep, mock_get):
#         with patch('builtins.print') as mocked_print:
#             search_and_download_photos(['nature'], total_photos=1, folder='/fake/folder', log_file='content/downloaded_pexel_photos.txt')
#             mocked_print.assert_called_with('[Error]: Rate limit exceeded for tag: nature. Sleeping for 60 seconds...')
#             mock_sleep.assert_called_with(60)

#     @patch('modules.download.download_pexel.requests.get')
#     def test_search_and_download_photos_no_photos_found(self, mock_get):
#         # Mock API response with no photos
#         mock_response = unittest.mock.Mock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {'photos': []}
#         mock_get.return_value = mock_response

#         with patch('builtins.print') as mocked_print:
#             search_and_download_photos(['unknown_tag'], total_photos=1, folder='/fake/folder', log_file='content/downloaded_pexel_photos.txt')
#             mocked_print.assert_any_call('No photos found for tag: unknown_tag')
#             mocked_print.assert_any_call('0 new photos downloaded and logged.')

#     @patch('modules.download.download_pexel.requests.get', side_effect=requests.exceptions.RequestException)
#     @patch('modules.download.download_pexel.os.makedirs')
#     def test_search_and_download_photos_request_exception(self, mock_makedirs, mock_get):
#         with patch('builtins.print') as mocked_print:
#             search_and_download_photos(['nature'], total_photos=1, folder='/fake/folder', log_file='content/downloaded_pexel_photos.txt')
#             mocked_print.assert_called_with("[Error]: Request exception for tag 'nature': ")

#     @patch('modules.download.download_pexel.requests.get')
#     @patch('modules.download.download_pexel.download_photo')
#     def test_search_and_download_photos_skip_duplicates(self, mock_download_photo, mock_get):
#         # Mock API response
#         mock_response = unittest.mock.Mock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             'photos': [
#                 {'id': 123456, 'src': {'original': 'http://example.com/photo1.jpg'}},
#                 {'id': 234567, 'src': {'original': 'http://example.com/photo2.jpg'}}
#             ]
#         }
#         mock_get.return_value = mock_response

#         with patch('modules.download.download_pexel.read_downloaded_photo_ids', return_value={'123456'}):
#             search_and_download_photos(['nature'], total_photos=2, folder='/fake/folder', log_file='content/downloaded_pexel_photos.txt')
#             mock_download_photo.assert_called_once_with('http://example.com/photo2.jpg', '/fake/folder', '234567')

#     def test_search_and_download_photos_invalid_total_photos(self):
#         with self.assertRaises(TypeError):
#             search_and_download_photos(['nature'], total_photos='five')

# if __name__ == '__main__':
#     unittest.main()