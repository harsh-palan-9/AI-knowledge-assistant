"""
Comprehensive test suite for document upload routes and services
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException, UploadFile
from io import BytesIO
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.routes.document import router as document_router
from app.services.document_service import save_file, read_pdf, read_txt, split_text, process_document
from langchain_core.documents import Document


class TestDocumentRoutes:
    """Test document upload routes"""
    
    def test_upload_pdf_success(self, client, mock_pdf_file, mock_user_info):
        """Test successful PDF upload"""
        with patch('app.dependencies.auth_dependency.verify_token', return_value=mock_user_info):
            with patch('app.services.document_service.save_file') as mock_save:
                mock_save.return_value = "uploads/test.pdf"
                
                with patch('app.services.document_service.process_document') as mock_process:
                    mock_process.return_value = (["chunk1", "chunk2"], [[0.1, 0.2, 0.3]])
                    
                    response = client.post(
                        "/document/upload/",
                        files={"file": ("test.pdf", mock_pdf_file.file, "application/pdf")},
                        headers={"Authorization": "Bearer test_token"}
                    )
                    
                    assert response.status_code == 200
                    assert response.json()["message"] == "File uploaded successfully"
    
    def test_upload_txt_success(self, client, mock_txt_file, mock_user_info):
        """Test successful TXT upload"""
        with patch('app.dependencies.auth_dependency.verify_token', return_value=mock_user_info):
            with patch('app.services.document_service.save_file') as mock_save:
                mock_save.return_value = "uploads/test.txt"
                
                with patch('app.services.document_service.process_document') as mock_process:
                    mock_process.return_value = (["chunk1", "chunk2"], [[0.1, 0.2, 0.3]])
                    
                    response = client.post(
                        "/document/upload/",
                        files={"file": ("test.txt", mock_txt_file.file, "text/plain")},
                        headers={"Authorization": "Bearer test_token"}
                    )
                    
                    assert response.status_code == 200
    
    def test_upload_unsupported_file_type(self, client, mock_unsupported_file, mock_user_info):
        """Test upload with unsupported file type"""
        with patch('app.dependencies.auth_dependency.verify_token', return_value=mock_user_info):
            response = client.post(
                "/document/upload/",
                files={"file": ("test.docx", mock_unsupported_file.file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 400
            assert "Unsupported file type" in response.json()["detail"]
    
    def test_upload_no_file(self, client, mock_user_info):
        """Test upload without file"""
        with patch('app.dependencies.auth_dependency.verify_token', return_value=mock_user_info):
            response = client.post(
                "/document/upload/",
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 422
    
    def test_upload_unauthorized(self, client, mock_pdf_file):
        """Test upload without authentication"""
        with patch('app.dependencies.auth_dependency.verify_token', side_effect=HTTPException(401, "Unauthorized")):
            response = client.post(
                "/document/upload/",
                files={"file": ("test.pdf", mock_pdf_file.file, "application/pdf")}
            )
            
            assert response.status_code == 401
    
    def test_upload_empty_filename(self, client, mock_user_info):
        """Test upload with empty filename"""
        with patch('app.dependencies.auth_dependency.verify_token', return_value=mock_user_info):
            empty_file = UploadFile(filename="", file=BytesIO(b""))
            
            response = client.post(
                "/document/upload/",
                files={"file": ("", empty_file.file, "application/pdf")},
                headers={"Authorization": "Bearer test_token"}
            )
            
            # Empty filename should be caught by the file type check or validation
            assert response.status_code in [400, 422]


class TestDocumentService:
    """Test document service functions"""
    
    def test_save_file_pdf(self, tmp_path, mock_pdf_file):
        """Test saving a PDF file"""
        with patch('app.services.document_service.UPLOAD_DIR', str(tmp_path)):
            file_path = save_file(mock_pdf_file)
            
            assert os.path.exists(file_path)
            assert file_path.endswith("test.pdf")
    
    def test_save_file_txt(self, tmp_path, mock_txt_file):
        """Test saving a TXT file"""
        with patch('app.services.document_service.UPLOAD_DIR', str(tmp_path)):
            file_path = save_file(mock_txt_file)
            
            assert os.path.exists(file_path)
            assert file_path.endswith("test.txt")
    
    def test_save_file_creates_directory(self, tmp_path):
        """Test that save_file creates directory if it doesn't exist"""
        upload_dir = tmp_path / "new_uploads"
        with patch('app.services.document_service.UPLOAD_DIR', str(upload_dir)):
            mock_file = UploadFile(filename="test.txt", file=BytesIO(b"test content"))
            
            file_path = save_file(mock_file)
            
            assert os.path.exists(upload_dir)
            assert os.path.exists(file_path)
    
    def test_read_pdf_success(self, tmp_path):
        """Test reading a PDF file"""
        from pypdf import PdfWriter
        
        # Create a simple PDF
        pdf_path = tmp_path / "test.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        
        with open(pdf_path, "wb") as f:
            writer.write(f)
        
        text = read_pdf(str(pdf_path))
        
        assert isinstance(text, str)
    
    def test_read_txt_success(self, tmp_path):
        """Test reading a TXT file"""
        txt_path = tmp_path / "test.txt"
        test_content = "This is test content\nWith multiple lines"
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        text = read_txt(str(txt_path))
        
        assert text == test_content
    
    def test_read_txt_encoding(self, tmp_path):
        """Test reading TXT with different encodings"""
        txt_path = tmp_path / "test.txt"
        test_content = "Test content with special chars: áéíóú"
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        text = read_txt(str(txt_path))
        
        assert "áéíóú" in text
    
    def test_split_text(self):
        """Test text splitting functionality"""
        long_text = "This is a test. " * 50  # Create long text
        chunks = split_text(long_text)
        
        assert len(chunks) > 1
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_split_text_short(self):
        """Test splitting short text"""
        short_text = "Short text"
        chunks = split_text(short_text)
        
        assert len(chunks) >= 1
    
    def test_process_document_pdf(self, tmp_path):
        """Test processing a PDF document"""
        from pypdf import PdfWriter
        
        # Create a simple PDF
        pdf_path = tmp_path / "test.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        
        with open(pdf_path, "wb") as f:
            writer.write(f)
        
        with patch('app.services.document_service.vector_store') as mock_store:
            mock_store.add_documents = Mock()
            
            result = process_document(str(pdf_path))
            
            assert "num_chunks" in result
            assert "message" in result
            mock_store.add_documents.assert_called_once()
    
    def test_process_document_txt(self, tmp_path):
        """Test processing a TXT document"""
        txt_path = tmp_path / "test.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("This is test content for processing.")
        
        with patch('app.services.document_service.vector_store') as mock_store:
            mock_store.add_documents = Mock()
            
            result = process_document(str(txt_path))
            
            assert "num_chunks" in result
            assert "message" in result
            mock_store.add_documents.assert_called_once()
    
    def test_process_document_unsupported_type(self, tmp_path):
        """Test processing an unsupported file type"""
        doc_path = tmp_path / "test.docx"
        with open(doc_path, "w") as f:
            f.write("fake content")
        
        with pytest.raises(ValueError) as exc_info:
            process_document(str(doc_path))
        
        assert "Unsupported file type" in str(exc_info.value)
    
    def test_split_text_creates_documents(self):
        """Test that split_text creates proper Document objects"""
        text = "This is test content. " * 10
        chunks = split_text(text)
        
        documents = [Document(page_content=chunk) for chunk in chunks]
        
        assert len(documents) == len(chunks)
        assert all(doc.page_content == chunk for doc, chunk in zip(documents, chunks))


class TestDocumentServiceEdgeCases:
    """Test edge cases for document service"""
    
    def test_save_file_overwrite(self, tmp_path):
        """Test saving a file that already exists"""
        with patch('app.services.document_service.UPLOAD_DIR', str(tmp_path)):
            mock_file = UploadFile(filename="test.txt", file=BytesIO(b"first content"))
            
            file_path1 = save_file(mock_file)
            
            # Save again with different content
            mock_file2 = UploadFile(filename="test.txt", file=BytesIO(b"second content"))
            file_path2 = save_file(mock_file2)
            
            assert file_path1 == file_path2
            assert os.path.exists(file_path2)
    
    def test_read_empty_pdf(self, tmp_path):
        """Test reading an empty PDF"""
        from pypdf import PdfWriter
        
        pdf_path = tmp_path / "empty.pdf"
        writer = PdfWriter()
        
        with open(pdf_path, "wb") as f:
            writer.write(f)
        
        text = read_pdf(str(pdf_path))
        
        assert text == ""
    
    def test_read_empty_txt(self, tmp_path):
        """Test reading an empty TXT file"""
        txt_path = tmp_path / "empty.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("")
        
        text = read_txt(str(txt_path))
        
        assert text == ""
    
    def test_split_text_empty_string(self):
        """Test splitting an empty string"""
        chunks = split_text("")
        
        # Should return at least one chunk or handle gracefully
        assert isinstance(chunks, list)
    
    def test_split_text_special_characters(self):
        """Test splitting text with special characters"""
        text = "Test with special chars: áéíóú ñ € ©\nNewlines\tTabs"
        chunks = split_text(text)
        
        assert len(chunks) >= 1
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_process_document_with_vector_store_error(self, tmp_path):
        """Test processing document when vector store fails"""
        txt_path = tmp_path / "test.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("Test content")
        
        with patch('app.services.document_service.vector_store') as mock_store:
            mock_store.add_documents.side_effect = Exception("Vector store error")
            
            with pytest.raises(Exception):
                process_document(str(txt_path))
    
    def test_save_file_large_content(self, tmp_path):
        """Test saving a large file"""
        large_content = b"x" * (10 * 1024 * 1024)  # 10 MB
        
        with patch('app.services.document_service.UPLOAD_DIR', str(tmp_path)):
            mock_file = UploadFile(filename="large.txt", file=BytesIO(large_content))
            
            file_path = save_file(mock_file)
            
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) == len(large_content)
    
    def test_read_txt_nonexistent_file(self):
        """Test reading a non-existent TXT file"""
        with pytest.raises(FileNotFoundError):
            read_txt("nonexistent_file.txt")
    
    def test_read_pdf_nonexistent_file(self):
        """Test reading a non-existent PDF file"""
        with pytest.raises(Exception):
            read_pdf("nonexistent_file.pdf")


class TestDocumentIntegration:
    """Integration tests for document upload workflow"""
    
    def test_full_upload_workflow_pdf(self, client, mock_pdf_file, mock_user_info, tmp_path):
        """Test complete PDF upload workflow"""
        with patch('app.dependencies.auth_dependency.verify_token', return_value=mock_user_info):
            with patch('app.services.document_service.UPLOAD_DIR', str(tmp_path)):
                with patch('app.services.document_service.vector_store') as mock_store:
                    mock_store.add_documents = Mock()
                    
                    response = client.post(
                        "/document/upload/",
                        files={"file": ("test.pdf", mock_pdf_file.file, "application/pdf")},
                        headers={"Authorization": "Bearer test_token"}
                    )
                    
                    assert response.status_code == 200
                    assert "num_chunks" in response.json()
    
    def test_full_upload_workflow_txt(self, client, mock_txt_file, mock_user_info, tmp_path):
        """Test complete TXT upload workflow"""
        with patch('app.dependencies.auth_dependency.verify_token', return_value=mock_user_info):
            with patch('app.services.document_service.UPLOAD_DIR', str(tmp_path)):
                with patch('app.services.document_service.vector_store') as mock_store:
                    mock_store.add_documents = Mock()
                    
                    response = client.post(
                        "/document/upload/",
                        files={"file": ("test.txt", mock_txt_file.file, "text/plain")},
                        headers={"Authorization": "Bearer test_token"}
                    )
                    
                    assert response.status_code == 200
                    assert "num_chunks" in response.json()
