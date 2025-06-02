import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from integrations.google_drive import GoogleDriveIntegration

@pytest.fixture
def mock_drive_service():
    return Mock()

@pytest.fixture
def mock_credentials():
    return Mock(valid=True, expired=False)

@pytest.fixture
def sample_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        tmp_file.write('Test content')
        tmp_file.flush()
        path = tmp_file.name
    yield path
    os.unlink(path)

@patch('integrations.google_drive.build')
@patch('integrations.google_drive.Credentials')
def test_upload_file(mock_creds, mock_build, mock_drive_service, sample_file):
    # Mock the drive service
    mock_build.return_value = mock_drive_service
    
    # Mock file creation response
    mock_drive_service.files().create().execute.return_value = {
        'id': 'test_file_id',
        'name': 'test_file.txt',
        'webViewLink': 'https://drive.google.com/test_file'
    }
    
    drive = GoogleDriveIntegration()
    result = drive.upload_file(sample_file)
    
    assert result['id'] == 'test_file_id'
    assert result['name'] == 'test_file.txt'
    assert result['link'] == 'https://drive.google.com/test_file'

@patch('integrations.google_drive.build')
@patch('integrations.google_drive.Credentials')
def test_create_folder(mock_creds, mock_build, mock_drive_service):
    # Mock the drive service
    mock_build.return_value = mock_drive_service
    
    # Mock folder creation response
    mock_drive_service.files().create().execute.return_value = {
        'id': 'test_folder_id',
        'name': 'Test Folder',
        'webViewLink': 'https://drive.google.com/test_folder'
    }
    
    drive = GoogleDriveIntegration()
    result = drive.create_folder('Test Folder')
    
    assert result['id'] == 'test_folder_id'
    assert result['name'] == 'Test Folder'
    assert result['link'] == 'https://drive.google.com/test_folder'

@patch('integrations.google_drive.build')
@patch('integrations.google_drive.Credentials')
def test_upload_file_to_folder(mock_creds, mock_build, mock_drive_service, sample_file):
    # Mock the drive service
    mock_build.return_value = mock_drive_service
    
    # Mock file creation response
    mock_drive_service.files().create().execute.return_value = {
        'id': 'test_file_id',
        'name': 'test_file.txt',
        'webViewLink': 'https://drive.google.com/test_file'
    }
    
    drive = GoogleDriveIntegration()
    result = drive.upload_file(sample_file, folder_id='test_folder_id')
    
    # Verify the file was uploaded with the correct folder ID
    create_call = mock_drive_service.files().create.call_args
    assert create_call[1]['body']['parents'] == ['test_folder_id']

@patch('integrations.google_drive.build')
@patch('integrations.google_drive.Credentials')
def test_error_handling(mock_creds, mock_build, mock_drive_service):
    # Mock the drive service
    mock_build.return_value = mock_drive_service
    
    # Mock an API error
    mock_drive_service.files().create().execute.side_effect = Exception('API Error')
    
    drive = GoogleDriveIntegration()
    
    # Test folder creation error handling
    with pytest.raises(Exception) as exc_info:
        drive.create_folder('Test Folder')
    assert str(exc_info.value) == 'API Error'
    
    # Test file upload error handling
    with tempfile.NamedTemporaryFile() as tmp_file:
        with pytest.raises(Exception) as exc_info:
            drive.upload_file(tmp_file.name)
        assert str(exc_info.value) == 'API Error'

@patch('integrations.google_drive.build')
@patch('integrations.google_drive.Credentials')
def test_safe_filename_handling(mock_creds, mock_build, mock_drive_service):
    # Mock the drive service
    mock_build.return_value = mock_drive_service
    
    # Create a file with special characters in the name
    with tempfile.NamedTemporaryFile(prefix='test!@#$%^&*', suffix='.txt', delete=False) as tmp_file:
        tmp_file.write(b'Test content')
        tmp_file.flush()
        path = tmp_file.name
    
    try:
        drive = GoogleDriveIntegration()
        drive.upload_file(path)
        
        # Verify the filename was sanitized in the API call
        create_call = mock_drive_service.files().create.call_args
        filename = create_call[1]['body']['name']
        
        # Only alphanumeric and safe characters should remain
        assert all(c.isalnum() or c in '-_. ' for c in filename)
    finally:
        os.unlink(path)
