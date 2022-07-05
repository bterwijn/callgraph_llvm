
def main():
    groups=Groups();

    data=[ ( [] ,0),
           ( ["a::"] ,1),
           ( ["b::"] ,2),
           ( ["c::"] ,3)
          ]
    
    data=[ ( [] ,0),
           ( ["std::"] ,1),
           ( ["std::","bla::"] ,2),
           ( ["std::","bla::"] ,3),
           ( ["std::","bla::"] ,4),
           ( ["std::","b::"] ,5),
           ( ["std::","b::"] ,6),
           ( ["std::"] ,7),
           ( ["other::","a::"] ,8),
           ( ["other::","b::","c::","d::"] ,9),
           ( ["other::","X::","b::","c::","d::"] ,10)
          ]

    for i in data:
        groups.add(*i)

    print(groups)
    
    for g in groups:
        print(g)
    

class Groups:

    def __init__(self):
        self.ids=set()
        self.subgroups={}

    def __repr__(self):
        return f"ids:{self.ids} subgroups{self.subgroups}"

    def add(self,group_list,id):
        if group_list:
            group_name=group_list[0]
            if not group_name in self.subgroups:
                self.subgroups[group_name]=Groups()
            self.subgroups[group_name].add(group_list[1:],id)
        else:
            self.ids.add(id)

    def __iter__(self):
        return Groups_Iter(self)

class Groups_Iter:

    def __init__(self,group):
        self.stack=[ (group, iter(group.subgroups)) ]
        self.group_name=[]

    def __next__(self):
        if len(self.stack)==0:
            raise StopIteration
        group,subgroup_iter=self.stack[-1]
        ids=group.ids
        group_name=self.group_name[:]
        stepping=True
        while stepping:
            try:
                group,subgroup_iter=self.stack[-1]
                subgroup_name=next(subgroup_iter)
                subgroup=group.subgroups[subgroup_name]
                self.stack.append( (subgroup,iter(subgroup.subgroups)) )
                self.group_name.append(subgroup_name)
                stepping=False
            except StopIteration:
                if self.group_name:
                    self.group_name.pop()
                if self.stack:
                    self.stack.pop()
                    if len(self.stack)==0:
                        stepping=False
        return (group_name,ids)

if __name__ == "__main__":
    main()
