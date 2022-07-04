import re

def fix_label(label):
    result=label.replace('<','\<')
    return result.replace('>','\>')

def get_name(label):
    result = re.search('.*label="{(.*)}".*', label)
    return result.group(1)

class Callgraph:

    def __init__(self,filename):
        self.nodes={}
        self.labels={}
        self.groups={}
        self.edges=[]
        self.read(filename)

    def __repr__(self):
        return f"nodes: {self.nodes}\ngroups: {self.groups}\nedges: {self.edges}"

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
                            label=fix_label(get_name(split[1]))
                            self.add_node(id,label)
                        elif len(split)==3:
                            self.edges.append((split[0],split[1],split[2]))
                line_nr+=1

    def add_node(self,id,label,group=""):
        self.labels[label]=id
        self.nodes[id]=label
        if not group in self.groups:
            self.groups[group]=[]
        self.groups[group].append(id)
        
    def merge(self,other):
        translate={}
        for id,label in other.nodes.items():
            if label in self.labels:
                translate[id]=self.labels[label]
            else:
                self.add_node(id,label)
        for i0,i1,i2 in other.edges:
            if i0 in translate:
                i0=translate[i0]
            if i2 in translate:
                i2=translate[i2]
            self.edges.append((i0,i1,i2))
            
    def group(self):
        old_groups=self.groups
        self.groups={}
        for group,ids in old_groups.items():
            for id in ids:
                label=self.nodes[id]
                splits=label.split(':')
                group=''.join(splits[:-1])
                label=splits[-1]
                self.add_node(id,label,group)

    def write(self,filename,label="default"):
        with open(filename, 'w') as file:
            self.write_header(file,label)
            self.write_body(file)
            self.write_footer(file)
            
    def write_header(self,file,label):
        file.write(f'digraph "{label}" {{\n')
        file.write(f'   label="Call graph: {label}";\n\n')
                
    def write_body(self,file):
        cluster=0
        for group,ids in self.groups.items():
            if not group=="":
                file.write(f"\nsubgraph cluster_{cluster} {{\n")
                file.write(f'   label = "{group}";\n')
                cluster+=1
            for id in ids:
                label=self.nodes[id]
                file.write(f'   {id} [shape=record,label="{{{label}}}"];\n')
            if not group=="":
                file.write("}\n")
        for i in self.edges:
            file.write(f"   {i[0]} {i[1]} {i[2]};\n")
        file.write("\n")
                
    def write_footer(self,file):
        file.write("}\n")
