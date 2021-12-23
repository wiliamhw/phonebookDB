import shelve
import uuid
import sqlite3
import random
from faker import Faker

# For debugging purpose
# import sys
# sys.stdout = sys.stderr

class PhoneBook:
    def __init__(self):
        self.namafile = 'phonebook.db'
        self.db = sqlite3.connect(self.namafile)
        self.db.execute(
            '''CREATE TABLE IF NOT EXISTS phonebook
            (id    TEXT PRIMARY KEY NOT NULL,
            nama   TEXT             NOT NULL,
            alamat INT              NOT NULL,
            notelp TEXT);'''
        )
        self.db.row_factory = sqlite3.Row
        if (self.count() == 0):
            print(self.seed())

    def list(self):
        data = []
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM phonebook')
            data = [dict(row) for row in cursor.fetchall()]
            cursor.close()

            return dict(status='OK',data=data)
        except Exception as e:
            print (e)
            return dict(status='ERR',msg='Error')

    def create(self,info):
        try:
            id = str(uuid.uuid1())

            self.db.execute('INSERT INTO phonebook (id, nama, alamat, notelp) \
                VALUES(?, ?, ?, ?)', 
                (id, info['nama'], info['alamat'], info['notelp'],)) 
            self.db.commit()

            return dict(status='OK',id=id)
        except Exception as e:
            print (e)
            return dict(status='ERR',msg='Tidak bisa Create')

    def delete(self,id):
        try:
            self.db.execute("DELETE FROM phonebook WHERE id = ?", (id,))
            self.db.commit()

            return dict(status='OK',msg='{} deleted' . format(id), id=id)
        except Exception as e:
            print (e)
            return dict(status='ERR',msg='Tidak bisa Delete')

    def update(self,id,info):
        try:
            updated_field = ''
            first = True

            for field in info:
                if not first:
                    updated_field += ', '
                else:
                    first = False

                updated_field += field + " = '" + info[field] + "' "

            self.db.execute('UPDATE phonebook SET ' + updated_field + " where id = '" + id + "'")
            self.db.commit()
            return dict(status='OK',msg='{} updated' . format(id), id=id)
        except Exception as e:
            print (e)
            return dict(status='ERR',msg='Tidak bisa Update')

    def read(self,id):
        try:
            data = None

            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM phonebook where id = ?', (id,)) 
            data = dict(cursor.fetchone())
            cursor.close()
            
            return dict(status='OK',data=data)
        except Exception as e:
            print (e)
            return dict(status='ERR',msg='Tidak Ketemu')

    def seed(self, rows = 5):
        fake = Faker()

        for i in range(rows):
            id = 'fe437958-2fa4-11eb-bf35-7fc0bd24c845' if i == 0 else str(uuid.uuid1())

            self.db.execute('INSERT INTO phonebook (id, nama, alamat, notelp) \
                VALUES(?, ?, ?, ?)', 
                (id, fake.name(), fake.address(), str(random.randint(9999,99999999))))
        self.db.commit()
        return 'Seeding success'

    def count(self):
        data = None
        cursor = self.db.cursor()
        cursor.execute('SELECT COUNT(*) FROM phonebook') 
        data = cursor.fetchone()[0]
        return data


if __name__=='__main__':
    pd = PhoneBook()
