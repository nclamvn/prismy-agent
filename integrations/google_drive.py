from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import io
import pickle
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class GoogleDriveIntegration:
    """Handle Google Drive integration for file upload and download"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    TOKEN_PATH = 'token.pickle'
    CREDENTIALS_PATH = 'credentials.json'
    
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        try:
            if os.path.exists(self.TOKEN_PATH):
                with open(self.TOKEN_PATH, 'rb') as token:
                    self.creds = pickle.load(token)
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists(self.CREDENTIALS_PATH):
                        raise FileNotFoundError(
                            "credentials.json not found. Please download it from Google Cloud Console."
                        )
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.CREDENTIALS_PATH, self.SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)
                
                with open(self.TOKEN_PATH, 'wb') as token:
                    pickle.dump(self.creds, token)
            
            self.service = build('drive', 'v3', credentials=self.creds)
            logger.info("Successfully authenticated with Google Drive")
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise
    
    def upload_file(self, file_path: str, folder_id: Optional[str] = None) -> Dict[str, Any]:
        """Upload a file to Google Drive"""
        try:
            file_metadata = {
                'name': os.path.basename(file_path),
                'parents': [folder_id] if folder_id else []
            }
            
            media = MediaFileUpload(
                file_path,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            logger.info(f"File uploaded successfully: {file.get('name')}")
            return {
                'id': file.get('id'),
                'name': file.get('name'),
                'link': file.get('webViewLink')
            }
            
        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            raise
    
    def download_file(self, file_id: str, output_path: str) -> bool:
        """Download a file from Google Drive"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.info(f"Download progress: {int(status.progress() * 100)}%")
            
            fh.seek(0)
            with open(output_path, 'wb') as f:
                f.write(fh.read())
                f.flush()
            
            logger.info(f"File downloaded successfully to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download file: {e}")
            return False
    
    def list_files(self, folder_id: Optional[str] = None, 
                   file_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """List files in Google Drive folder"""
        try:
            query_parts = []
            
            if folder_id:
                query_parts.append(f"'{folder_id}' in parents")
            
            if file_types:
                mime_types = [f"mimeType='{mime}'" for mime in file_types]
                query_parts.append(f"({' or '.join(mime_types)})")
            
            query = ' and '.join(query_parts) if query_parts else None
            
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            return [{
                'id': f.get('id'),
                'name': f.get('name'),
                'type': f.get('mimeType'),
                'link': f.get('webViewLink')
            } for f in files]
            
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []
    
    def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new folder in Google Drive"""
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id] if parent_id else []
            }
            
            file = self.service.files().create(
                body=file_metadata,
                fields='id, name, webViewLink'
            ).execute()
            
            logger.info(f"Folder created successfully: {folder_name}")
            return {
                'id': file.get('id'),
                'name': file.get('name'),
                'link': file.get('webViewLink')
            }
            
        except Exception as e:
            logger.error(f"Failed to create folder: {e}")
            raise
