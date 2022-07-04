
CPPS        = $(wildcard *.cpp)
LLVMS       = $(patsubst %.cpp,%.llvm,$(CPPS))
DOTS_RAW    = $(patsubst %.cpp,%.llvm.callgraph.dot,$(CPPS))
DOTS        = $(patsubst %.cpp,%.dot,$(CPPS))
PNGS        = $(patsubst %.cpp,%.png,$(CPPS))

all: $(PNGS)

clean:
	rm -f $(LLVMS) $(DOTS_RAW) $(DOTS) $(PNGS)

%.llvm: %.cpp
	clang++ -S -emit-llvm $< -o $@

%.llvm.callgraph.dot: %.llvm
	opt $< -enable-new-pm=0 -analyze -dot-callgraph

%.dot: %.llvm.callgraph.dot
	cat $< | c++filt > $@

%.png:	%.dot
	cat $< | dot -Tpng -o $@


