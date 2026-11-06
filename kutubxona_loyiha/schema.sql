PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS readers (id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, phone TEXT UNIQUE, registered_at TEXT DEFAULT CURRENT_DATE);
CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL, publication_year INTEGER, copies_total INTEGER NOT NULL CHECK(copies_total >= 0));
CREATE TABLE IF NOT EXISTS loans (id INTEGER PRIMARY KEY, reader_id INTEGER NOT NULL REFERENCES readers(id), book_id INTEGER NOT NULL REFERENCES books(id), loan_date TEXT NOT NULL DEFAULT CURRENT_DATE, due_date TEXT NOT NULL, return_date TEXT, CHECK (due_date >= loan_date), CHECK (return_date IS NULL OR return_date >= loan_date));
CREATE INDEX IF NOT EXISTS idx_loans_reader ON loans(reader_id);
CREATE INDEX IF NOT EXISTS idx_loans_book ON loans(book_id);
