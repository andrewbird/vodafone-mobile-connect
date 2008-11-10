PROG=usb_modeswitch

$(PROG): $(PROG).c
	$(CC) -o $@ -lusb $< 

install: $(PROG)
	strip $<
	install -D -s $<	$(DESTDIR)/usr/sbin/$<
	install -D $(PROG).conf $(DESTDIR)/etc/$(PROG).conf
	
clean:
	rm -f $(PROG)

