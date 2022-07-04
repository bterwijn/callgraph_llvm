
CPPS        = $(wildcard *.cpp)
LLVMS       = $(patsubst %.cpp,%.llvm,$(CPPS))
DOTS_RAW    = $(patsubst %.cpp,%.llvm.callgraph.dot,$(CPPS))
DOTS        = $(patsubst %.cpp,%.dot,$(CPPS))
PNGS        = $(patsubst %.cpp,%.png,$(CPPS))
PDFS        = $(patsubst %.cpp,%.pdf,$(CPPS))

all: $(DOTS) $(PDFS)

clean:
	rm -f $(DOTS) $(PDFS)

%.llvm: %.cpp                           # generate a llvm from a source file
	clang++ -S -emit-llvm $< -o $@

%.llvm.callgraph.dot: %.llvm            # generate a raw-dot file from a llvm
	opt $< -enable-new-pm=0 -analyze -dot-callgraph

%.dot: %.llvm.callgraph.dot             # demangle names in raw-dot file to dot file
	cat $< | c++filt > $@

%.png:	%.dot                           # generate a png from a dot file
	cat $< | dot -Tpng -o $@

%.pdf:	%.dot                           # generate a pdf from a dot file
	cat $< | dot -Tpdf -o $@
