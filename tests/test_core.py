import unittest
import os
import shutil
import tempfile
from core.organizer import organize_files, undo_last_operation, MODE_ROOT, MODE_FLATTEN, MODE_RECURSIVE, IGNORED_FOLDERS

class TestOrganizer(unittest.TestCase):
    def setUp(self):
        # Create temp dir
        self.test_dir = tempfile.mkdtemp()
        
        # Create test files
        self.create_test_file("document.txt")
        self.create_test_file("image.jpg")
        
        # Create subfolder with files (for Flatten/Recursive tests)
        self.sub_dir = os.path.join(self.test_dir, "Subfolder")
        os.makedirs(self.sub_dir)
        self.create_test_file("sub_doc.txt", folder=self.sub_dir)
        
        # Create IGNORED folder (e.g., node_modules)
        self.ignored_dir = os.path.join(self.test_dir, "node_modules")
        os.makedirs(self.ignored_dir)
        self.create_test_file("sensitive.js", folder=self.ignored_dir)
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
        
    def create_test_file(self, filename, folder=None):
        if folder is None:
            folder = self.test_dir
        with open(os.path.join(folder, filename), 'w') as f:
            f.write("content")

    def test_root_organization(self):
        """Test ROOT mode organization"""
        log = organize_files(self.test_dir, mode=MODE_ROOT)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "document.txt")))
        # Ignored folder should be untouched
        self.assertTrue(os.path.exists(os.path.join(self.ignored_dir, "sensitive.js")))

    def test_flatten_organization(self):
        """Test FLATTEN mode with Ignore List"""
        log = organize_files(self.test_dir, mode=MODE_FLATTEN)
        
        # Normal files moved
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "document.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "sub_doc.txt")))
        
        # Ignored folder files should NOT be moved
        self.assertTrue(os.path.exists(os.path.join(self.ignored_dir, "sensitive.js")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "Code", "sensitive.js")))

    def test_recursive_organization(self):
        """Test RECURSIVE mode with Ignore List"""
        log = organize_files(self.test_dir, mode=MODE_RECURSIVE)
        
        # Normal files moved
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "document.txt")))
        
        # Ignored folder should NOT be organized internally
        # (Assuming sensitive.js would go to 'Code' if organized)
        self.assertTrue(os.path.exists(os.path.join(self.ignored_dir, "sensitive.js")))
        self.assertFalse(os.path.exists(os.path.join(self.ignored_dir, "Code", "sensitive.js")))

    def test_conflict_resolution(self):
        """Test conflict resolution"""
        target_dir = os.path.join(self.test_dir, "Images")
        os.makedirs(target_dir)
        with open(os.path.join(target_dir, "image.jpg"), 'w') as f:
            f.write("existing content")
            
        organize_files(self.test_dir, mode=MODE_ROOT)
        
        self.assertTrue(os.path.exists(os.path.join(target_dir, "image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(target_dir, "image_copy_1.jpg")))

    def test_undo(self):
        """Test Undo"""
        log = organize_files(self.test_dir, mode=MODE_ROOT)
        undo_last_operation(log)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "document.txt")))

if __name__ == '__main__':
    unittest.main()
