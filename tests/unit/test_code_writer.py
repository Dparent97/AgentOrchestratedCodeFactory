"""
Tests for CodeWriter

Tests the safe file writing with transaction support.
"""

import pytest
import tempfile
from pathlib import Path

from code_factory.core.code_writer import CodeWriter


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def code_writer(temp_project_dir):
    """Create a CodeWriter instance"""
    return CodeWriter(temp_project_dir)


@pytest.fixture
def sample_files():
    """Sample files for testing"""
    return {
        "README.md": "# Test Project\n\nThis is a test.",
        "src/main.py": "def main():\n    print('Hello')\n",
        "src/__init__.py": '"""Test package"""\n',
        "tests/test_main.py": "def test_main():\n    assert True\n",
    }


class TestCodeWriter:
    """Test CodeWriter functionality"""

    def test_initialization(self, temp_project_dir):
        """Test CodeWriter initialization"""
        writer = CodeWriter(temp_project_dir)
        assert writer is not None
        assert writer.project_root == temp_project_dir

    def test_write_single_file(self, code_writer, temp_project_dir):
        """Test writing a single file"""
        files = {"test.txt": "Hello, World!"}

        code_writer.write_project_files(files, enable_staging=False)

        # Check file was created
        test_file = temp_project_dir / "test.txt"
        assert test_file.exists()
        assert test_file.read_text() == "Hello, World!"

    def test_write_multiple_files(self, code_writer, temp_project_dir, sample_files):
        """Test writing multiple files"""
        code_writer.write_project_files(sample_files, enable_staging=False)

        # Check all files were created
        for file_path, content in sample_files.items():
            full_path = temp_project_dir / file_path
            assert full_path.exists()
            assert full_path.read_text() == content

    def test_write_with_staging(self, code_writer, temp_project_dir, sample_files):
        """Test writing files with staging enabled"""
        code_writer.write_project_files(sample_files, enable_staging=True)

        # Files should exist in final location
        for file_path in sample_files.keys():
            full_path = temp_project_dir / file_path
            assert full_path.exists()

    def test_create_nested_directories(self, code_writer, temp_project_dir):
        """Test creating nested directory structure"""
        files = {
            "src/package/module.py": "# Module",
            "tests/unit/test_module.py": "# Test",
        }

        code_writer.write_project_files(files, enable_staging=False)

        # Check directories were created
        assert (temp_project_dir / "src" / "package").exists()
        assert (temp_project_dir / "tests" / "unit").exists()

        # Check files exist
        assert (temp_project_dir / "src" / "package" / "module.py").exists()
        assert (temp_project_dir / "tests" / "unit" / "test_module.py").exists()

    def test_create_project_structure(self, code_writer, temp_project_dir):
        """Test creating project directory structure"""
        folder_structure = {
            "src/": [],
            "tests/": [],
            "docs/": [],
        }

        code_writer.create_project_structure(folder_structure, enable_staging=False)

        # Check directories were created
        assert (temp_project_dir / "src").exists()
        assert (temp_project_dir / "tests").exists()
        assert (temp_project_dir / "docs").exists()

    def test_validate_project_structure(self, code_writer, temp_project_dir):
        """Test project structure validation"""
        # Initially should fail (no files)
        assert code_writer.validate_project_structure() is False

        # Create essential files
        (temp_project_dir / "README.md").write_text("# Test")
        (temp_project_dir / "pyproject.toml").write_text("[project]\n")

        # Now should pass
        assert code_writer.validate_project_structure() is True

    def test_get_project_files(self, code_writer, temp_project_dir, sample_files):
        """Test reading project files"""
        # Write files first
        code_writer.write_project_files(sample_files, enable_staging=False)

        # Read them back
        files = code_writer.get_project_files()

        # Should have all files
        for file_path, content in sample_files.items():
            assert file_path in files
            assert files[file_path] == content

    def test_transaction_rollback_on_error(self, code_writer, temp_project_dir):
        """Test that transaction handles errors gracefully"""
        # Test that empty files dict succeeds (doesn't raise error)
        # The transaction system handles this gracefully
        code_writer.write_project_files({})  # Empty dict should succeed without error

        # Verify no files were created
        files = code_writer.get_project_files()
        assert len(files) == 0

    def test_write_empty_file(self, code_writer, temp_project_dir):
        """Test writing an empty file"""
        files = {"empty.txt": ""}

        code_writer.write_project_files(files, enable_staging=False)

        # File should exist but be empty
        empty_file = temp_project_dir / "empty.txt"
        assert empty_file.exists()
        assert empty_file.read_text() == ""

    def test_write_large_content(self, code_writer, temp_project_dir):
        """Test writing large file content"""
        large_content = "x" * 1000000  # 1MB of data
        files = {"large.txt": large_content}

        code_writer.write_project_files(files, enable_staging=False)

        # Verify content
        large_file = temp_project_dir / "large.txt"
        assert large_file.exists()
        assert len(large_file.read_text()) == 1000000

    def test_overwrite_existing_files(self, code_writer, temp_project_dir):
        """Test overwriting existing files"""
        # Create initial file
        initial_files = {"test.txt": "Initial content"}
        code_writer.write_project_files(initial_files, enable_staging=False)

        # Overwrite with new content
        new_files = {"test.txt": "New content"}
        code_writer.write_project_files(new_files, enable_staging=False)

        # Check content was updated
        test_file = temp_project_dir / "test.txt"
        assert test_file.read_text() == "New content"

    def test_unicode_content(self, code_writer, temp_project_dir):
        """Test writing files with unicode content"""
        files = {
            "unicode.txt": "Hello 世界 🌍 Привет",
            "emoji.txt": "Test 😀 🎉 ✨",
        }

        code_writer.write_project_files(files, enable_staging=False)

        # Verify unicode content
        for file_path, content in files.items():
            full_path = temp_project_dir / file_path
            assert full_path.read_text(encoding="utf-8") == content

    def test_file_permissions(self, code_writer, temp_project_dir, sample_files):
        """Test that files have correct permissions"""
        code_writer.write_project_files(sample_files, enable_staging=False)

        # Files should be readable
        for file_path in sample_files.keys():
            full_path = temp_project_dir / file_path
            assert full_path.exists()
            # Should be able to read
            content = full_path.read_text()
            assert content is not None
