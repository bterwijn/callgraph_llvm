import Groups
import re

def main():
    label="std::more::other::name"
    namespaces,name=get_namespaces_and_name(label)
    print(namespaces,name)
    print(join_namespaces(namespaces))
    
class Callgraph:

    def __init__(self,filename):
        self.nodes={}
        self.labels={}
        self.groups=Groups.Groups()
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
                            print("label:",label)
                            #if not "std::" in label or not "_gnu" in label:    # --------------------------- block a lot
                            self.add_node(id,label)
                            #else:
                            #    print("ignore label:",label)
                line_nr+=1

    def add_node(self,id,label,group_list=[]):
        self.labels[label]=id
        self.nodes[id]=label
        self.groups.add(group_list,id)
        #print("add:",group_list,label)
        
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
        self.groups=Groups.Groups()
        for group_list,ids in old_groups:
            for id in ids:
                label=self.nodes[id]
                namespaces,name=get_namespaces_and_name(label)
                self.add_node(id,label,namespaces)

    def write(self,filename,label="default"):
        with open(filename, 'w') as file:
            self.write_header(file,label)
            self.write_body(file)
            self.write_footer(file)
            
    def write_header(self,file,label):
        file.write(f'digraph "{label}" {{\n')
        file.write(f'   label="Call graph: {label}";\n\n')

    def close_curly_brace(self,file,prev_group_list,group_list,indent):
        i=len(prev_group_list)-1
        while i>=0 and (i>=len(group_list) or prev_group_list[i]!=group_list[i]):
            file.write(indent*(i+1)+"}\n")
            i-=1
        
    def write_body(self,file):
        cluster=0
        indent="    "
        selected_ids=set()
        group_list_index=0
        prev_group_list=[]
        for group_list,ids in self.groups:
            self.close_curly_brace(file,prev_group_list,group_list,indent)
            prev_group_list=group_list[:]
            if group_list:
                file.write("\n")
                file.write(indent*len(group_list)+f"subgraph cluster_{cluster} {{\n")
                file.write(indent*len(group_list)+indent+f'label = "{group_list[-1]}";\n')
                cluster+=1
            for id in ids:
                label=self.nodes[id]
                namespaces,name=get_namespaces_and_name(label)
                file.write(indent*len(group_list)+indent+f'{id} [shape=record,label="{{{name}}}"];\n')
                selected_ids.add(id)
        self.close_curly_brace(file,prev_group_list,[],indent)
                
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

def get_namespaces_and_name(label):
    namespaces=[]
    count0=0 # ( )
    count1=0 # < >
    count2=0 # [ ]
    prev_i=0
    for i in range(len(label)):
        if label[i]=='(':
            count0+=1
        elif label[i]==')':
            count0-=1
        elif label[i]=='<':
            count1+=1
        elif label[i]=='>':
            count1-=1
        elif label[i]=='[':
            count2+=1
        elif label[i]==']':
            count2-=1
        elif i>0 and label[i]==':' and label[i-1]==':' and count0==0 and count1==0 and count2==0:
            namespaces.append(label[prev_i:i+1])
            prev_i=i+1
    name=label[prev_i:]
    return (namespaces,label[prev_i:])
    
def join_namespaces(namespaces):
    return "".join(namespaces)

if __name__ == "__main__":
    main()
