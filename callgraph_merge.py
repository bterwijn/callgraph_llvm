import Callgraph
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
    callgraph_first=None
    for filename in filenames:
        callgraph = Callgraph.Callgraph(filename)
        if callgraph_first is None:
            callgraph_first=callgraph
        else:
            callgraph_first.merge(callgraph)
    if not callgraph_first is None:
        callgraph_first.write(output,label)

main()
