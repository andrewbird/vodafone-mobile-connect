DATADIR = /usr/share/
LOCALEDIR = $(DATADIR)/locale
DOMAIN = VMC

all: create mo install

#create pot file
create:
	xgettext -d$(DOMAIN) -LGlade `find ../glade -name "*.glade"` -o $(DOMAIN).pot
	xgettext --from-code=utf-8 -k_ -d$(DOMAIN) -LPython `find ../.. -name "*.py"` -o $(DOMAIN).pot -j

#update all po fles
update-po: $(DOMAIN).pot
	for po in *.po; do \
		lingua=`basename $$po .po`; \
	        mv $$lingua.po $$lingua.old.po; \
		if msgmerge -o $$lingua.po $$lingua.old.po $(DOMAIN).pot; then \
		    rm $$lingua.old.po; \
		else \
		    rm -f $$lingua.po; \
		    mv $$lingua.old.po $$lingua.po; \
		fi \
	done

#create all mo files
mo:
	for po in *.po; do \
		lingua=`basename $$po .po` ; \
		msgfmt -cf -o $$lingua.mo $$po ; \
		mkdir -p locale/$$lingua/LC_MESSAGES/ ; \
		ln -f $$lingua.mo locale/$$lingua/LC_MESSAGES/$(DOMAIN).mo ; \
	done

#install mo files
install: mo
	for mo in *.mo; do \
		lingua=`basename $$mo .mo`; \
		install -D --mode=644 $$lingua.mo $(DESTDIR)/$(LOCALEDIR)/$$lingua/LC_MESSAGES/$(DOMAIN).mo ; \
	done

clean:
	rm -Rf locale
	rm -f *.mo
