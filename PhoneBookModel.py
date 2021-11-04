import shelve
import uuid
import os

class PhoneBook:
    def __init__(self):
        self.namafile = 'phonebook.db'
        self.db = shelve.open(self.namafile,writeback=True)
    def list(self):
        data = []
        try:
            for i in self.db.keys():
                data.append(dict(id=i,data=self.db[i]))
            return dict(status='OK',data=data)
        except:
            return dict(status='ERR',msg='Error')
    def create(self,info):
        try:
            id = str(uuid.uuid1())
            self.db[id] = info
            return dict(status='OK',id=id)
        except:
            return dict(status='ERR',msg='Tidak bisa Create')
    def delete(self,id):
        try:
            del self.db[id]
            return dict(status='OK',msg='{} deleted' . format(id), id=id)
        except:
            return dict(status='ERR',msg='Tidak bisa Delete')
    def update(self,id,info):
        try:
            self.db[id]=info
            return dict(status='OK',msg='{} updated' . format(id), id=id)
        except:
            return dict(status='ERR',msg='Tidak bisa Update')
    def read(self,id):
        try:
            return dict(status='OK',id=id,data=self.db[id])
        except:
            return dict(status='ERR',msg='Tidak Ketemu')
    def measure(self):
# kita ingin menggunakan file size yang digunakan untuk menyimpan record (phonebook.db)
# dan jumlah record yang digunakan
        file = os.stat(self.namafile)
        file_size = file.st_size  #dalam bytes
        jumlah_record = len(self.db.keys())
        return dict(status="OK",data=dict(size=file_size,record=jumlah_record))



if __name__=='__main__':
    pd = PhoneBook()
#    ----------- create
#    result = pd.create(dict(nama='royyana',alamat='ketintang',notelp='6212345'))
#    print(result)
#    result = pd.create(dict(nama='ibrahim',alamat='ketintang',notelp='6212341'))
#    print(result)
#    result = pd.create(dict(nama='Ananda', alamat='Dinoyo Sekolahan', notelp='6212345'))
#    print(result)
#    ------------ list
    print(pd.list())
    print(pd.measure())
#    ------------ info
#    print(pd.read('c516b780-2fa2-11eb-bf35-7fc0bd24c845'))



