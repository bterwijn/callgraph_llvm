import sys

def main():
    output="default.dot"
    label="default-label"
    filenames=[]
    i=1
    if len(sys.argv)<2:
        help()
    while i<len(sys.argv):
        if sys.argv[i]=="-h":
            help()
        elif sys.argv[i]=="-o":
            output=sys.argv[i+1]
            i+=1
        elif sys.argv[i]=="-l":
            label=sys.argv[i+1]
            i+=1
        else:
            filenames.append(sys.argv[i])
        i+=1
    merge_files(filenames,output,label)

def help():
    print("usage: python merge_dots.py <options> <filenames>")
    print("  options: -h                     print help")
    print("           -o <output-file>       set output file")
    print("           -l <label>             set label")
    
def merge_files(filenames,output,label):
    first=None
    for filename in filenames:
        dot_file = Dot_File(filename)
        if first is None:
            first=dot_file
        else:
            first.merge(dot_file)
    if not first is None:
        first.write(output,label)
        
class Dot_File:

    def __init__(self,filename):
        self.nodes={}
        self.edges=[]
        self.read(filename)

    def __repr__(self):
        return f"nodes: {self.nodes}\nedges: {self.edges}"

    def read(self,filename):
        with open(filename) as f:
            line_nr=0
            for line in f:
                line=line.strip()
                if line_nr==0:
                    pass
                elif line_nr==1:
                    pass
                else:
                    if line=='}':
                        pass
                    elif len(line)>0 and line[-1]==';':
                        line=line[0:-1]
                        split = line.split()
                        if len(split)==2:
                            self.nodes[split[1]]=split[0]
                        elif len(split)==3:
                            self.edges.append((split[0],split[1],split[2]))
                line_nr+=1

    def merge(self,other):
        translate={}
        for name,id in other.nodes.items():
            if name in self.nodes:
                translate[id]=self.nodes[name]
            else:
                self.nodes[name]=id
        for i0,i1,i2 in other.edges:
            if i0 in translate:
                i0=translate[i0]
            if i2 in translate:
                i2=translate[i2]
            self.edges.append((i0,i1,i2))

    def write(self,filename,label="default"):
        with open(filename, 'w') as file:
            self.write_header(file,label)
            self.write_body(file)
            self.write_footer(file)
            
    def write_header(self,file,label):
        file.write(f'digraph "{label}" {{\n')
        file.write(f'   label="Call graph: {label}";\n\n')
                
    def write_body(self,file):
        for name,id in self.nodes.items():
            file.write(f"   {id} {name};\n")
        for i in self.edges:
            file.write(f"   {i[0]} {i[1]} {i[2]};\n")
        file.write("\n")
                
    def write_footer(self,file):
        file.write("}\n")

main()
