import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from app import setup,connect,available_books,borrow,return_book,readers,add_reader,add_book,active_loans,backup,restore

class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/'test.db'
        setup(self.path,demo=True)
        self.con=connect(self.path)
        self.future=(date.today()+timedelta(days=14)).isoformat()
    def tearDown(self):
        self.con.close(); self.tmp.cleanup()
    def test_seed_data(self):
        self.assertEqual(len(readers(self.con)),15)
        self.assertEqual(len(available_books(self.con)),10)
    def test_borrow_return(self):
        before=available_books(self.con)[0][3]
        loan=borrow(self.con,1,1,self.future)
        self.assertEqual(available_books(self.con)[0][3],before-1)
        return_book(self.con,loan)
        self.assertEqual(available_books(self.con)[0][3],before)
    def test_invalid_date(self):
        for value in ['4','2026-99-99','2020-01-01']:
            with self.subTest(value=value),self.assertRaises(ValueError): borrow(self.con,1,1,value)
    def test_unknown_reader(self):
        with self.assertRaises(ValueError): borrow(self.con,999,1,self.future)
    def test_unknown_book(self):
        with self.assertRaises(ValueError): borrow(self.con,1,999,self.future)
    def test_no_more_copies(self):
        borrow(self.con,1,3,self.future);borrow(self.con,2,3,self.future)
        with self.assertRaises(ValueError): borrow(self.con,3,3,self.future)
    def test_add_reader_and_search(self):
        new_id=add_reader(self.con,'Yangi Talaba','900000001')
        self.assertEqual(readers(self.con,'Yangi')[0][0],new_id)
    def test_add_book(self):
        book=add_book(self.con,'Test kitob','Test muallif',4)
        self.assertEqual(next(x[3] for x in available_books(self.con) if x[0]==book),4)
    def test_double_return(self):
        loan=borrow(self.con,1,1,self.future);return_book(self.con,loan)
        with self.assertRaises(ValueError):return_book(self.con,loan)
    def test_active_loans(self):
        loan=borrow(self.con,1,1,self.future)
        self.assertIn(loan,[r[0] for r in active_loans(self.con)])
    def test_backup_restore(self):
        path=Path(self.tmp.name)/'backup.db'
        backup(self.path,path)
        add_reader(self.con,'Vaqtinchalik','900000002')
        self.con.close()
        restore(path,self.path)
        self.con=connect(self.path)
        self.assertEqual(len(readers(self.con)),15)
    def test_duplicate_phone(self):
        with self.assertRaises(Exception):add_reader(self.con,'Boshqa','901112233')

if __name__=='__main__': unittest.main()
