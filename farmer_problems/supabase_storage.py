"""
Supabase Storage Integration for Farmer Problems
Handles image uploads to Supabase storage bucket
"""

import os
import uuid
from django.conf import settings
from supabase import create_client, Client
import mimetypes
from pathlib import Path


class SupabaseStorageService:
    """Service for managing Supabase storage operations"""
    
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.bucket_name = settings.SUPABASE_STORAGE_BUCKET
        
        if not self.supabase_key:
            raise ValueError("SUPABASE_KEY not configured in settings")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    def upload_image(self, file, folder='problems', filename=None):
        """
        Upload an image to Supabase storage
        
        Args:
            file: Django UploadedFile object
            folder: Folder name in bucket (e.g., 'problems', 'solutions')
            filename: Optional custom filename
        
        Returns:
            dict: {'success': bool, 'url': str, 'path': str, 'error': str}
        """
        try:
            # Generate unique filename if not provided
            if not filename:
                ext = Path(file.name).suffix
                filename = f"{uuid.uuid4()}{ext}"
            
            # Create full path
            file_path = f"{folder}/{filename}"
            
            # Read file content
            file_content = file.read()
            
            # Determine content type
            content_type = file.content_type or mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
            
            # Upload to Supabase
            response = self.client.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_content,
                file_options={
                    "content-type": content_type,
                    "cache-control": "3600",
                    "upsert": "false"
                }
            )
            
            # Get public URL
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            
            return {
                'success': True,
                'url': public_url,
                'path': file_path,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'url': None,
                'path': None,
                'error': str(e)
            }
    
    def upload_multiple_images(self, files, folder='problems'):
        """
        Upload multiple images
        
        Args:
            files: List of Django UploadedFile objects
            folder: Folder name in bucket
        
        Returns:
            list: List of upload results
        """
        results = []
        for file in files:
            result = self.upload_image(file, folder)
            results.append(result)
        return results
    
    def delete_image(self, file_path):
        """
        Delete an image from Supabase storage
        
        Args:
            file_path: Full path of file in bucket
        
        Returns:
            dict: {'success': bool, 'error': str}
        """
        try:
            self.client.storage.from_(self.bucket_name).remove([file_path])
            return {
                'success': True,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_multiple_images(self, file_paths):
        """
        Delete multiple images
        
        Args:
            file_paths: List of file paths
        
        Returns:
            dict: {'success': bool, 'deleted_count': int, 'error': str}
        """
        try:
            self.client.storage.from_(self.bucket_name).remove(file_paths)
            return {
                'success': True,
                'deleted_count': len(file_paths),
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'deleted_count': 0,
                'error': str(e)
            }
    
    def get_public_url(self, file_path):
        """
        Get public URL for a file
        
        Args:
            file_path: Path of file in bucket
        
        Returns:
            str: Public URL
        """
        return self.client.storage.from_(self.bucket_name).get_public_url(file_path)
    
    def list_files(self, folder=''):
        """
        List files in a folder
        
        Args:
            folder: Folder path
        
        Returns:
            list: List of file objects
        """
        try:
            files = self.client.storage.from_(self.bucket_name).list(folder)
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def create_bucket_if_not_exists(self):
        """
        Create the storage bucket if it doesn't exist
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            # Check if bucket exists
            buckets = self.client.storage.list_buckets()
            bucket_exists = any(b.name == self.bucket_name for b in buckets)
            
            if not bucket_exists:
                # Create bucket
                self.client.storage.create_bucket(
                    self.bucket_name,
                    options={"public": True}
                )
                return {
                    'success': True,
                    'message': f'Bucket {self.bucket_name} created successfully'
                }
            else:
                return {
                    'success': True,
                    'message': f'Bucket {self.bucket_name} already exists'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error creating bucket: {str(e)}'
            }


# Singleton instance
_storage_service = None

def get_storage_service():
    """Get or create storage service instance"""
    global _storage_service
    if _storage_service is None:
        _storage_service = SupabaseStorageService()
    return _storage_service

