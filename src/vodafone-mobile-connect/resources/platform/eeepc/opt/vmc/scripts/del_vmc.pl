#!/usr/bin/perl -w

while (<>) {
	if(/\/vmc.desktop/) { # skip section
		do {
			$_=<STDIN>;
		} until(/\/parcel/);

		do {
			$_=<STDIN>;
		} until(/</);
	}
	print;
}


