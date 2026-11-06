"""Kutubxona ma'lumotlar bazasining sodda konsol dasturi."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def connect(db_path='library.db'):
    connection = sqlite3.connect(db_path)
    connection.execute('PRAGMA foreign_keys = ON')
    return connection

def setup(db_path='library.db', demo=False):
    with connect(db_path) as con:
        con.executescript((ROOT / 'schema.sql').read_text(encoding='utf-8'))
        if demo:
            count = con.execute('SELECT COUNT(*) FROM books').fetchone()[0]
            if count == 0:
                con.executescript((ROOT / 'sample_data.sql').read_text(encoding='utf-8'))

def available_books(con):
    return con.execute('''SELECT b.id,b.title,b.author,b.copies_total - COUNT(l.id) AS available
        FROM books b LEFT JOIN loans l ON b.id=l.book_id AND l.return_date IS NULL
        GROUP BY b.id ORDER BY b.id''').fetchall()

def borrow(con, reader_id, book_id, due_date):
    if not con.execute('SELECT 1 FROM readers WHERE id=?',(reader_id,)).fetchone():
        raise ValueError('O‘quvchi topilmadi')
    if not con.execute('SELECT 1 FROM books WHERE id=?',(book_id,)).fetchone():
        raise ValueError('Kitob topilmadi')
    free = next(row[3] for row in available_books(con) if row[0] == book_id)
    if free <= 0:
        raise ValueError('Bo‘sh nusxa yo‘q')
    with con:
        con.execute('INSERT INTO loans(reader_id,book_id,due_date) VALUES (?,?,?)',(reader_id,book_id,due_date))

def return_book(con, loan_id):
    with con:
        result = con.execute('UPDATE loans SET return_date=CURRENT_DATE WHERE id=? AND return_date IS NULL',(loan_id,))
        if result.rowcount == 0:
            raise ValueError('Faol berilgan kitob topilmadi')

def main():
    setup(demo=True)
    with connect() as con:
        while True:
            print('\n1. Kitoblar  2. O‘quvchilar  3. Kitob berish  4. Qaytarish  0. Chiqish')
            option = input('Tanlang: ').strip()
            try:
                if option == '1':
                    for row in available_books(con): print(row)
                elif option == '2':
                    for row in con.execute('SELECT id,full_name,phone FROM readers'): print(row)
                elif option == '3':
                    borrow(con,int(input('O‘quvchi ID: ')),int(input('Kitob ID: ')),input('Qaytarish muddati (YYYY-MM-DD): '))
                    print('Kitob berildi')
                elif option == '4':
                    return_book(con,int(input('Berish ID: '))); print('Kitob qaytarildi')
                elif option == '0': break
                else: print('Noto‘g‘ri tanlov')
            except (ValueError,sqlite3.Error) as error:
                print('Xatolik:',error)

if __name__ == '__main__':
    main()
