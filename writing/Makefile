.PHONY: default pdf show spellcheck clean mrproper

NAME = thesis
DEPS = literature.bib

# build the pdf and display it
default: $(NAME).pdf show

# build our pdf
%.pdf: %.tex $(DEPS)
	rubber --unsafe --pdf $<

# simply build the pdf without showing it
# this target is for convenience, allowing to type `make pdf`
# instead of `make filename.pdf`
pdf: $(NAME).pdf

# display the generated pdf using evince
show: $(NAME).pdf
	evince $(NAME).pdf &

# use aspell, a spellchecking tool, to check the tex file
# for spelling errors.
# Note: make sure to have desired aspell dictionaries installed
spellcheck:
	aspell -t -c $(NAME).tex

# use rubber's cleaning functionality
clean:
	rubber --clean *.tex

# rubber --clean doesn't remove pdf or bak files
mrproper: clean
	rm -f *.pdf
	rm -f *.bak
