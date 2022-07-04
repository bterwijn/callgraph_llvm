
def fix_label(label):
    result=label.replace('<','\<')
    return result.replace('>','\>')

class Callgraph:

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
                            id=split[0]
                            label=fix_label(split[1])
                            self.nodes[label]=id
                        elif len(split)==3:
                            self.edges.append((split[0],split[1],split[2]))
                line_nr+=1

    def merge(self,other):
        translate={}
        for label,id in other.nodes.items():
            if label in self.nodes:
                translate[id]=self.nodes[label]
            else:
                self.nodes[label]=id
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
