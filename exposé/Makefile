.PHONY: default view spellcheck clean mrproper

NAME = exposé
DEPS = ../literature.bib

default: $(NAME).pdf show

$(NAME).pdf: $(NAME).tex $(DEPS)
	rubber --pdf $(NAME)

show: $(NAME).pdf
	evince $(NAME).pdf &

spellcheck:
	aspell -t -c $(NAME).tex

clean:
	rubber --clean $(NAME)

mrproper: clean
	rm -f $(NAME).pdf
