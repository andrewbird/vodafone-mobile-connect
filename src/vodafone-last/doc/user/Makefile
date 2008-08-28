export SP_ENCODING=XML

all: es en

html: en-html
es: es-pdf es-html
en: en-pdf en-html

es-html:
	docbook2html manual.es.xml
	mkdir user-es
	cp -R images user-es
	mv *html user-es
	find user-es -name '.svn' | xargs rm -rf
	mv user-es ../guide/

es-pdf:
	docbook2pdf manual.es.xml
	mv manual.es.pdf user-es.pdf

en-html:
	docbook2html manual.en.xml
	mkdir user-en
	cp -R images user-en
	mv *html user-en
	find user-en -name '.svn' | xargs rm -rf
	mv user-en ../guide/user

en-pdf:
	docbook2pdf manual.en.xml
	mv manual.en.pdf user-en.pdf

clean:
	echo "Clean"
