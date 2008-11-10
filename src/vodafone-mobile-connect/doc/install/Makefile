export SP_ENCODING=XML

all: en

html: en-html
en: en-pdf en-html

en-html:
	docbook2html install.en.xml
	mkdir install-en
	cp -R images install-en
	mv *html install-en
	find install-en -name '.svn' | xargs rm -rf
	mv install-en ../guide/install

en-pdf:
	docbook2pdf install.en.xml
	mv install.en.pdf install-en.pdf

clean:
	echo "Clean"
