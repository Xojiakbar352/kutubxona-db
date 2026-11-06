import tempfile
import unittest
from pathlib import Path
from app import setup,connect,available_books,borrow,return_book

class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name) / 'test.db')
        setup(self.path,demo=True)
        self.con = connect(self.path)
    def tearDown(self):
        self.con.close()
        self.tmp.cleanup()
    def test_initial_books(self):
        self.assertEqual(len(available_books(self.con)),3)
    def test_borrow_and_return(self):
        before = available_books(self.con)[0][3]
        borrow(self.con,2,1,'2026-12-31')
        self.assertEqual(available_books(self.con)[0][3],before-1)
        loan_id = self.con.execute('SELECT MAX(id) FROM loans').fetchone()[0]
        return_book(self.con,loan_id)
        self.assertEqual(available_books(self.con)[0][3],before)
    def test_unknown_reader(self):
        with self.assertRaises(ValueError): borrow(self.con,999,1,'2026-12-31')
    def test_no_more_copies(self):
        borrow(self.con,1,3,'2026-12-31')
        with self.assertRaises(ValueError): borrow(self.con,2,3,'2026-12-31')

if __name__ == '__main__': unittest.main()
