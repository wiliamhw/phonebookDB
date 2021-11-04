import shelve
import uuid
import docker
import hashlib





class Provisioning:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.namafile = 'users.db'
        self.db = shelve.open(self.namafile,writeback=True)
    def list(self):
        data = []
        try:
            for i in self.db.keys():
                data.append(dict(id=i,data=self.db[i]))
            return dict(status='OK',data=data)
        except:
            return dict(status='ERR',msg='Error')
    def create(self,username,password):
        try:
            id = str(uuid.uuid1())
            self.db[id] = dict(username=username,password=hashlib.md5(password),port=11111,provision_status=False,info=dict())
            self.docker_client.containers.run("my-phonebook-service",detach=True,)


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



if __name__=='__main__':
    p = Provisioning()
    p.create('royyana','sukolilo4567')
