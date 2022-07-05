import re

def main():
    label="std::more::other::name"
    print(get_name(label))
    namespaces=get_namespaces(label)
    print(namespaces)
    print(join_namespaces(namespaces))

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
                    if len(line)>0 and line[-1]==';':
                        line=line[0:-1]
                        split = line.split()
                        if len(split)==3 and split[1]=='->':
                            self.edges.append((split[0],split[1],split[2]))
                        else:
                            id=split[0]
                            label=fix_label(get_label(" ".join(split[1:])))
                            #if not "std::" in label or not "_gnu" in label:    # --------------------------- block a lot
                            self.add_node(id,label)
                            #else:
                            #    print("ignore label:",label)
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
                name=get_name(label)
                namespaces=get_namespaces(label)
                group=join_namespaces(namespaces)
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
        selected_ids=set()
        for group,ids in self.groups.items():
            if not group=="":
                file.write(f"\nsubgraph cluster_{cluster} {{\n")
                file.write(f'   label = "{group}";\n')
                cluster+=1
            for id in ids:
                label=self.nodes[id]
                name=get_name(label)
                file.write(f'   {id} [shape=record,label="{{{name}}}"];\n')
                selected_ids.add(id)
            if not group=="":
                file.write("}\n")
        for i0,i1,i2 in self.edges:
            if i0 in selected_ids and i2 in selected_ids:
                file.write(f"   {i0} {i1} {i2};\n")
        file.write("\n")
                
    def write_footer(self,file):
        file.write("}\n")

def fix_label(label):
    result=label.replace('<','\<')
    return result.replace('>','\>')

def get_label(line):
    result = re.search('.*label="{(.*)}".*', line)
    return result.group(1)

def get_name(label):
    ni=label.rfind('::')
    if ni<0:
        return label
    else:
        return label[ni+2:]

def get_namespaces(label):
    split=[]
    i=0
    while True:
        ni=label.find('::',i)+2
        if ni<=1:
            break
        split.append(label[i:ni])
        i=ni
    return split

def join_namespaces(split):
    return "".join(split)

if __name__ == "__main__":
    main()
