import random
import shelve
import time
import uuid
import docker
import hashlib





class ProvisioningModel:
    def __init__(self):
        self.namafile = 'users.db'
        self.db = shelve.open(self.namafile,writeback=True)
        self.dbports = shelve.open('dbports.db',writeback=True)
    def nomor_ports_belum_dialokasikan(self,no_port=11111):
        try:
            return (no_port in self.dbports.keys()) is False
        except:
            return True
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
            docker_client = docker.from_env()
            id = str(uuid.uuid1())
            the_port=11111
            username = info['username']
            password = info['password']
            while True:
               the_port = random.randint(11111,22222)
               if (self.nomor_ports_belum_dialokasikan(the_port)):
                   break
               time.sleep(1)
            self.db[id] = dict(username=username,password=hashlib.md5(password.encode()).digest(),port=the_port,container_id=False,info=dict())
            container = docker_client.containers.run(name=f"PHONEBOOK-{the_port}",image="my-phonebook-service",environment=dict(USERNAME=username),ports={ '32000/tcp': the_port},detach=True)
            self.db[id]['port']=the_port
            self.db[id]['container_id']=container.id
            return dict(status='OK',id=id,container_id = str(container.id))
        except Exception as e:
            return dict(status='ERR',msg='Tidak bisa Create')
    def delete(self,id):
        try:
            del self.db[id]
            return dict(status='OK',msg='{} deleted' . format(id), id=id)
        except:
            return dict(status='ERR',msg='Tidak bisa Delete')
    def update(self,id,info):
        try:
            self.db[id]['info']=info
            return dict(status='OK',msg='{} updated' . format(id), id=id)
        except:
            return dict(status='ERR',msg='Tidak bisa Update')
    def read(self,id):
        try:
            return dict(status='OK',id=id,data=self.db[id])
        except:
            return dict(status='ERR',msg='Tidak Ketemu')



if __name__=='__main__':
    p = ProvisioningModel()
    cid = p.create(dict(username='royyana',password='kucinglucu1234'))
    print(cid)