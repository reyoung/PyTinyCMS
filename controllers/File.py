from BaseHandler import *
import model
F=model.File

class IndexHandler(BaseHandler):
    def get(self):
        self.write("READ")
    def post(self):
        self.write("CREATE")
class IdHandler(BaseHandler):
    def get(self,id):
        self.write('READ%s'%id)
    def put(self,id):
        self.write("UPDATE%s"%id)
    def delete(self,id):
        self.write("DELETE%s"%id)
        


#if __name__ == '__main__':
#    # Run Enity Unittest.
#    TestContent='Hello world'
#    TestTitle='hello.txt'
#    model.Init()
##    file = model.File.save_file(TestTitle, TestContent)
#    file = list(model.File.select(model.File.q.id==1))[0]
#    print file.load_file()