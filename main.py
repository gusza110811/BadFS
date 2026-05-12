# first prototype, only one table

from io import BufferedRandom
import struct
import shlex
import os

class BadFS:
    def __init__(self, disk:BufferedRandom):
        self.disk = disk
        self.load_table()
    
    def load_table(self):
        self.table = self.decode_table(self.read(-1))
    
    def save_table(self):
        self.write(-1,self.encode_table(self.table))
    
    def decode_table(self,raw_table:bytearray):
        def get_name(pos):
            end = raw_table.find(0, pos,pos+15)
            if end != -1:
                return raw_table[pos:end]
            else:
                return ""
        files = []
        for i in range(32):
            string = get_name(i*16)
            files.append(string.decode())
        return files

    def encode_table(self,table:list[str]):
        out = bytearray()
        for item in table:
            out.extend(struct.pack("16s",item.encode()))
        return out
    
    def read(self, index):
        self.disk.seek((index+2)*512)
        return self.disk.read(512)
    
    def write(self, index, data:bytearray|bytes):
        data = bytearray(data)
        length = len(data)
        if length > 512:
            data = data[:512]
        elif length < 512:
            data.extend(bytes(512-length))
        
        self.disk.seek((index+2)*512)
        self.disk.write(data)

    def delete(self,index):
        self.table[index] = ""
        self.save_table()
        self.load_table()
        return True
    
    def list(self):
        return self.table
    
    def find(self,name):
        files = self.table
        try:
            return files.index(name)
        except ValueError:
            return None

    def add_file(self,name):
        try:
            index = self.table.index("")
        except ValueError:
            return False
        self.table[index] = name
        self.save_table()
        self.load_table()
        return index

def test_interactive():

    if not os.path.isfile("disk.img"):
        disk = open("disk.img","wb+")
        disk.write(bytes(512*33))
    else:
        disk = open("disk.img","rb+")
    fs = BadFS(disk)

    while 1:
        command, *args = shlex.split(input("> "))
        try:
            match command:
                case "exit":
                    break
                case "ls":
                    print("\n".join([item for item in fs.list() if item]))
                case "cat":
                    index = fs.find(args[0])
                    if index is None:
                        print("not found")
                        continue
                    print(fs.read(index))
                case "rm":
                    index = fs.find(args[0])
                    fs.delete(index)
                case "touch":
                    index = fs.find(args[0])
                    if index is None:
                        index = fs.add_file(args[0])

                    fs.write(index,input("< ").encode())
                case "import":
                    source = args[0]
                    dest = args[1]
                    data = open(source,"rb").read()
                    index = fs.find(dest)
                    if index is None:
                        index = fs.add_file(dest)
                    fs.write(index,data)
                case "export":
                    source = args[0]
                    dest = args[1]

                    index = fs.find(source)
                    if index is None:
                        print("not found")
                        continue
                    data = fs.read(index)

                    with open(dest,"wb") as file:
                        file.write(data)
        
        except IndexError:
            print("not enough parameter")

if __name__ == "__main__":
    test_interactive()
