#!/usr/bin/perl -w

sub add_vmc() {
   print << 'EOF';
<parcel simplecat="Internet" shortcut="/usr/share/applications/vmc.desktop"
	icon="vodafone_norm.png" 
	selected_icon="vodafone_hi.png">
	<name lang="en">Mobile Connect</name>	
	<name lang="zh_TW">Mobile Connect</name>	
	<name lang="zh_HK">Mobile Connect</name>	
	<name lang="zh_CN">Mobile Connect</name>	
	<name lang="ar_AE">Mobile Connect</name>	
	<name lang="de_DE">Mobile Connect</name>	
	<name lang="es_AR">Mobile Connect</name>	
	<name lang="es_ES">Mobile Connect</name>	
	<name lang="fr_FR">Mobile Connect</name>	
	<name lang="it_IT">Mobile Connect</name>	
	<name lang="nl_NL">Mobile Connect</name>	
	<name lang="pt_PT">Mobile Connect</name>	
	<name lang="ru_RU">Mobile Connect</name>	
	<name lang="th_TH">Mobile Connect</name>	
	<name lang="tr_TR">Mobile Connect</name>	
	<name lang="ja_JP">Mobile Connect</name>	
	<name lang="ko_KR">Mobile Connect</name>	
	<name lang="cs_CZ">Mobile Connect</name>	
	<name lang="hu_HU">Mobile Connect</name>	
	<name lang="sk_SK">Mobile Connect</name>	
	<name lang="el_GR">Mobile Connect</name>	
	<name lang="pl_PL">Mobile Connect</name>	
</parcel>
EOF
}

while (<>) {
	if(/firefox.desktop/) { # insert after web icon
		print;
		do {
			$_=<STDIN>;
			print;
		} until(/\/parcel/);

		$_=<STDIN>;

		until(/</) {
			print;
			$_=<STDIN>;
		}

		add_vmc;

		print "\n\n\n";

		print;
	} else {
		print $_;
	}
}


