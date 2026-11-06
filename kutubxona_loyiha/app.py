"""Kutubxona boshqaruv tizimi — SQLite konsol ilovasi."""
import sqlite3
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'library.db'

def connect(db_path=DB):
    con = sqlite3.connect(db_path)
    con.execute('PRAGMA foreign_keys=ON')
    return con

def setup(db_path=DB, demo=False):
    with connect(db_path) as con:
        con.executescript((ROOT / 'schema.sql').read_text(encoding='utf-8'))
        if demo and con.execute('SELECT COUNT(*) FROM readers').fetchone()[0] == 0 and con.execute('SELECT COUNT(*) FROM books').fetchone()[0] == 0:
            con.executescript((ROOT / 'sample_data.sql').read_text(encoding='utf-8'))

def available_books(con):
    return con.execute('''SELECT b.id,b.title,b.author,b.copies_total - COUNT(l.id) AS available
      FROM books b LEFT JOIN loans l ON b.id=l.book_id AND l.return_date IS NULL
      GROUP BY b.id ORDER BY b.id''').fetchall()

def readers(con, search=''):
    return con.execute('SELECT id,full_name,phone FROM readers WHERE full_name LIKE ? ORDER BY id', ('%'+search+'%',)).fetchall()

def add_reader(con, name, phone):
    if not name.strip(): raise ValueError('Ism bo‘sh bo‘lmasligi kerak')
    if not phone.strip(): raise ValueError('Telefon bo‘sh bo‘lmasligi kerak')
    with con:
        return con.execute('INSERT INTO readers(full_name,phone) VALUES (?,?)',(name.strip(),phone.strip())).lastrowid

def add_book(con, title, author, copies):
    if not title.strip() or not author.strip(): raise ValueError('Kitob nomi va muallif majburiy')
    if copies < 0: raise ValueError('Nusxa soni manfiy bo‘lmasin')
    with con:
        return con.execute('INSERT INTO books(title,author,copies_total) VALUES (?,?,?)',(title.strip(),author.strip(),copies)).lastrowid

def borrow(con, reader_id, book_id, due_date):
    try: parsed = date.fromisoformat(due_date)
    except (ValueError,TypeError): raise ValueError('Sana YYYY-MM-DD ko‘rinishida bo‘lishi kerak') from None
    if parsed < date.today(): raise ValueError('Qaytarish muddati bugundan oldin bo‘lmasin')
    if not con.execute('SELECT 1 FROM readers WHERE id=?',(reader_id,)).fetchone(): raise ValueError('O‘quvchi topilmadi')
    if not con.execute('SELECT 1 FROM books WHERE id=?',(book_id,)).fetchone(): raise ValueError('Kitob topilmadi')
    free = next(row[3] for row in available_books(con) if row[0] == book_id)
    if free <= 0: raise ValueError('Bo‘sh nusxa yo‘q')
    with con:
        return con.execute('INSERT INTO loans(reader_id,book_id,due_date) VALUES (?,?,?)',(reader_id,book_id,due_date)).lastrowid

def active_loans(con):
    return con.execute('''SELECT l.id,r.full_name,b.title,l.due_date FROM loans l
      JOIN readers r ON r.id=l.reader_id JOIN books b ON b.id=l.book_id
      WHERE l.return_date IS NULL ORDER BY l.id''').fetchall()

def return_book(con, loan_id):
    with con:
        cur = con.execute('UPDATE loans SET return_date=CURRENT_DATE WHERE id=? AND return_date IS NULL',(loan_id,))
        if cur.rowcount == 0: raise ValueError('Faol berilgan kitob topilmadi')

def backup(db_path=DB, destination=None):
    destination = Path(destination) if destination else ROOT / 'backups' / f'library_{date.today().isoformat()}.db'
    destination.parent.mkdir(parents=True,exist_ok=True)
    if Path(db_path).resolve() == destination.resolve(): raise ValueError('Zaxira manzili asl baza bilan bir xil')
    with connect(db_path) as source, sqlite3.connect(destination) as target:
        source.backup(target)
    return destination

def restore(source, db_path=DB):
    source = Path(source)
    if not source.is_file(): raise ValueError('Zaxira fayli topilmadi')
    if source.resolve() == Path(db_path).resolve(): raise ValueError('Bir xil fayl')
    with sqlite3.connect(source) as check:
        if check.execute('PRAGMA integrity_check').fetchone()[0] != 'ok': raise ValueError('Zaxira fayli buzilgan')
        required = {'readers','books','loans'}
        existing = {r[0] for r in check.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not required.issubset(existing): raise ValueError('Bu kutubxona bazasi emas')
        with sqlite3.connect(db_path) as target: check.backup(target)

def show(rows):
    if not rows: print('Ma’lumot topilmadi')
    for row in rows: print(' | '.join(map(str,row)))

def main():
    setup(demo=True)
    while True:
        print('\n1.Kitoblar 2.O‘quvchilar 3.Kitob berish 4.Qaytarish 5.O‘quvchi qo‘shish')
        print('6.Kitob qo‘shish 7.O‘quvchi qidirish 8.Faol berishlar 9.Zaxira 10.Tiklash 0.Chiqish')
        option = input('Tanlang: ').strip()
        if option == '0': break
        try:
            if option == '10':
                source = input('Zaxira fayli manzili: ').strip()
                if input('Bazani zaxiradan almashtirasizmi? (ha/yo‘q): ').strip().lower() == 'ha':
                    restore(source); print('Baza tiklandi')
                continue
            with connect() as con:
                if option == '1': show(available_books(con))
                elif option == '2': show(readers(con))
                elif option == '3':
                    loan_id = borrow(con,int(input('O‘quvchi ID: ')),int(input('Kitob ID: ')),input('Qaytarish muddati (YYYY-MM-DD): ').strip())
                    print('Kitob berildi. Berish ID:',loan_id)
                elif option == '4':
                    show(active_loans(con))
                    return_book(con,int(input('Berish ID: '))); print('Kitob qaytarildi')
                elif option == '5': print('Yangi o‘quvchi ID:',add_reader(con,input('F.I.Sh.: '),input('Telefon: ')))
                elif option == '6': print('Yangi kitob ID:',add_book(con,input('Kitob nomi: '),input('Muallif: '),int(input('Nusxalar: '))))
                elif option == '7': show(readers(con,input('Ismdan qidirish: ')))
                elif option == '8': show(active_loans(con))
                elif option == '9': print('Zaxira yaratildi:',backup())
                else: print('Noto‘g‘ri tanlov')
        except (ValueError,sqlite3.Error,OSError) as error: print('Xatolik:',error)

if __name__ == '__main__': main()
