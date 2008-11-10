/*
  Mode switching tool for controlling flip flop (multiple device) USB gear
  Version 0.9.4, 2008/06/09

  Copyright (C) 2007, 2008 Josua Dietze (mail to "usb_admin" at the domain
  from the README; please do not post the complete address to The Net!
  Or write a personal message through the forum to "Josh")

  Command line parsing, decent usage/config output/handling and bugfixes added by:
    Joakim Wennergren (jokedst) (gmail.com)

  TargetClass parameter implementation to support new Option devices/firmware:
    Paul Hardwick (http://www.pharscape.org)

  Created with initial help from:
    "usbsnoop2libusb.pl" by Timo Lindfors (http://iki.fi/lindi/usb/usbsnoop2libusb.pl)

  Config file parsing stuff borrowed from:
    Guillaume Dargaud (http://www.gdargaud.net/Hack/SourceCode.html)

  Hexstr2bin function borrowed from:
    Jouni Malinen (http://hostap.epitest.fi/wpa_supplicant, from "common.c")

  Code, fixes and ideas from:
    Aki Makkonen
    Denis Sutter 
    Lucas Benedicic 
    Roman Laube 

  More contributors are listed in the config file.

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details:

  http://www.gnu.org/licenses/gpl.txt

*/

/* Recommended tab size: 4 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <signal.h>
#include <ctype.h>
#include <getopt.h>
#include <usb.h>
#include "usb_modeswitch.h"

#define LINE_DIM 1024

int write_bulk(int endpoint, char *message, int length);
int read_bulk(int endpoint, char *buffer, int length);

char *TempPP=NULL;

struct usb_dev_handle *devh;

int DefaultVendor=0, DefaultProduct=0, TargetVendor=0, TargetProduct=0, TargetClass=0;
int MessageEndpoint=0, ResponseEndpoint=0;
char DetachStorageOnly=0, NeedResponse=0, HuaweiMode=0, verbose=0, show_progress=1;
char MessageContent[LINE_DIM];

static struct option long_options[] =
{
    {"help",				no_argument,       0, 'h'},
    {"DefaultVendor",		required_argument, 0, 'v'},
    {"DefaultProduct",		required_argument, 0, 'p'},
    {"TargetVendor",		required_argument, 0, 'V'},
    {"TargetProduct",		required_argument, 0, 'P'},
    {"TargetClass",			required_argument, 0, 'C'},
    {"MessageEndpoint",		required_argument, 0, 'm'},
    {"MessageContent",		required_argument, 0, 'M'},
    {"ResponseEndpoint",	required_argument, 0, 'r'},
    {"DetachStorageOnly",	required_argument, 0, 'd'},
    {"HuaweiMode",			required_argument, 0, 'H'},
    {"NeedResponse",		required_argument, 0, 'n'},
    {"config",				required_argument, 0, 'c'},
    {"verbose",				no_argument, 0, 'W'},
    {"quiet",				no_argument, 0, 'Q'},
    {0, 0, 0, 0}
};

void readConfigFile(const char *configFilename)
{
    ParseParamHex(configFilename, TargetVendor);
    ParseParamHex(configFilename, TargetProduct);
    ParseParamHex(configFilename, TargetClass);
    ParseParamHex(configFilename, DefaultVendor);
    ParseParamHex(configFilename, DefaultProduct);
    ParseParamBool(configFilename, DetachStorageOnly);
    ParseParamBool(configFilename, HuaweiMode);
    ParseParamHex(configFilename, MessageEndpoint);
    ParseParamString(configFilename, MessageContent);
    ParseParamHex(configFilename, NeedResponse);
    ParseParamHex(configFilename, ResponseEndpoint);
}

void printConfig()
{
	printf ("DefaultVendor=0x%x\n",		DefaultVendor);
	printf ("DefaultProduct=0x%x\n",	DefaultProduct);
	printf ("TargetVendor=0x%x\n",		TargetVendor);
	printf ("TargetProduct=0x%x\n",		TargetProduct);
	printf ("TargetClass=0x%x\n",		TargetClass);
	printf ("DetachStorageOnly=%i\n",	(int)DetachStorageOnly);
	printf ("HuaweiMode=%i\n",			(int)HuaweiMode);
	printf ("MessageEndpoint=0x%x\n",	MessageEndpoint);
	printf ("MessageContent=\"%s\"\n",	MessageContent);
	printf ("NeedResponse=%i\n",		(int)NeedResponse);
	printf ("ResponseEndpoint=0x%x\n",	ResponseEndpoint);
	printf ("\n");
}

int readArguments(int argc, char **argv)
{
	int c, option_index = 0, count=0;
	if(argc==1) return 0;

	while (1)
	{
        c = getopt_long (argc, argv, "hWQv:p:V:P:C:m:M:r:d:H:n:c:",
                        long_options, &option_index);
    
        /* Detect the end of the options. */
        if (c == -1)
            break;
    	count++;
        switch (c)
		{
	        case 'v': DefaultVendor = strtol(optarg, NULL, 16); break;
	        case 'p': DefaultProduct = strtol(optarg, NULL, 16); break;
	        case 'V': TargetVendor = strtol(optarg, NULL, 16); break;
	        case 'P': TargetProduct = strtol(optarg, NULL, 16); break;
			case 'C': TargetClass = strtol(optarg, NULL, 16); break;
	        case 'm': MessageEndpoint = strtol(optarg, NULL, 16); break;
	        case 'M': strcpy(MessageContent, optarg); break;
	        case 'r': ResponseEndpoint = strtol(optarg, NULL, 16); break;
	        case 'd': DetachStorageOnly = (toupper(optarg[0])=='Y' || toupper(optarg[0])=='T'|| optarg[0]=='1'); break;
	        case 'H': HuaweiMode = (toupper(optarg[0])=='Y' || toupper(optarg[0])=='T'|| optarg[0]=='1'); break;
	        case 'n': NeedResponse = strtol(optarg, NULL, 16); break;
	        case 'c': readConfigFile(optarg); break;
	        case 'W': verbose=1; count--; break;
	        case 'Q': show_progress=0; count--; break;
    
	        case 'h':
	            printf ("Usage: usb_modeswitch [-hvpVPmMrdHn] [-c config-file]\n\n");
	            printf (" -h, --help                    this help\n");
	            printf (" -v, --DefaultVendor [nr]      set vendor number to look for\n");
	            printf (" -p, --DefaultProduct [nr]     set model number to look for\n");
	            printf (" -V, --TargetVendor [nr]       target vendor; if found, quit\n");
	            printf (" -P, --TargetProduct [nr]      target model, if found quit\n");
				printf (" -C, --TargetClass [nr]        target Device class, if found quit\n");
	            printf (" -m, --MessageEndpoint [nr]    where to write message\n");
	            printf (" -M, --MessageContent [nr]     message to send\n");
	            printf (" -n, --NeedResponse [1|0]      whether to try to read a response\n");
	            printf (" -r, --ResponseEndpoint [nr]   where to read response from\n");
	            printf (" -d, --DetachStorageOnly [1|0] whether to just detach the storage driver\n");
				printf (" -H, --HuaweiMode [1|0]        whether to just apply a special sequence\n");
	            printf (" -c, --config [config-file]    load named config file\n");
	            printf (" -Q, --quiet                   don't show progress or error messages\n");
	            printf (" -W, --verbose                 print all settings before running\n\n");
				exit(0);
	            break;
	    
	        default: //Unsupported - error message has already been printed
	            printf ("\n");
	            exit(1);
		}
	}

	return count;
}


int main(int argc, char **argv) {
    int ret, message_length, devclass;
	int numTargets = 0;
	int numDefaults = 0;
    char buf[65535];

    struct usb_device *dev;
    char ByteString[LINE_DIM/2];

	printf("\n * usb_modeswitch: tool for controlling \"flip flop\" mode USB devices\n");
   	printf(" * Version 0.9.4 (C) Josua Dietze 2008\n");
   	printf(" * Works with libusb 0.1.12 and probably other versions\n\n");

	// Check command arguments, use them instead of config file if possible
	switch (readArguments(argc, argv)) {
		case 1:
			if (!verbose && show_progress)
				break;
		case 0:
			readConfigFile("/etc/usb_modeswitch.conf");
			break;
		default:
			;
	}

	if (!show_progress) printf(" Quiet mode, no progress shown\n\n");

	if(verbose) printConfig();

    usb_init();
    usb_find_busses();
    usb_find_devices();

	if (!(DefaultVendor && DefaultProduct)) {
		if (show_progress) printf("No default vendor/product ID given. Aborting\n\n");
		exit(1);
	}

	if (TargetVendor && TargetProduct) {
		if (show_progress) printf("Looking for target devices\n");
		search_devices(&numTargets, TargetVendor, TargetProduct, TargetClass);
		if (numTargets) {
			if (show_progress) printf(" Found target devices (%d)\n", numTargets);
		} else {
			if (show_progress) printf(" No target device found\n");
		}
	}

    if (show_progress) printf("Looking for default devices\n");
    dev = search_devices(&numDefaults, DefaultVendor, DefaultProduct, TargetClass);
    if (numDefaults) {
		if (show_progress) printf(" Found default devices (%d)\n", numDefaults);
		if (TargetClass > 0) {
			if ( dev != NULL ) {
				if (show_progress) printf(" OK, found default device not in target class mode\n");
			} else {
				if (show_progress) printf(" All devices in target class mode\n");
			}
		}
	}
	if (dev != NULL) {
		if (show_progress) printf("Prepare switching, accessing latest device\n");
    } else {
		if (show_progress) printf(" No default device found. Is it connected? Bye\n\n");
		exit(0);
    }

    devh = usb_open(dev);
	if (devh == NULL) {
		if (show_progress) fprintf(stderr, "Error: could not access device. Aborting\n\n");
		exit(1);
	}
    
    signal(SIGTERM, release_usb_device);

#ifdef LIBUSB_HAS_GET_DRIVER_NP
    if ( !HuaweiMode ) {
	    if (show_progress) printf("Looking for active default driver to detach it\n");
	    ret = usb_get_driver_np(devh, 0, buf, sizeof(buf));
	    if (ret == 0) {
			if (show_progress) printf(" OK, driver found (\"%s\")\n", buf);
			if ( (DetachStorageOnly && !strcmp(buf,"usb-storage")) || !DetachStorageOnly ) {
#ifdef LIBUSB_HAS_DETACH_KERNEL_DRIVER_NP
				ret = usb_detach_kernel_driver_np(devh, 0);
				if (ret == 0) {
					if (show_progress) printf(" OK, Driver \"%s\" successfully detached\n", buf);
				} else {
					if (show_progress) printf(" Driver \"%s\" detach failed with error %d. Trying to continue ...\n", buf, ret);
				}
#else
					printf(" Driver detaching not possible on this platform. ");
					if (DetachStorageOnly)
						printf("Try to rmmod the usb-storage module!\n");
					else
						printf("Trying to continue ...\n");
#endif
			} else {
			    if (show_progress) printf(" No usb-storage driver found. Switching not necessary. Bye\n\n");
			    exit(0);
			}
	    } else {
			if (DetachStorageOnly) {
			    if (show_progress) printf(" No driver found. Driver probably detached already. Bye\n\n");
			    exit(0);
			} else
				if (show_progress) printf(" No driver found. Device probably not initialized. Trying to continue ...\n");
	    }
	}
#else
	printf(" Driver detection not possible on this platform. Trying to continue ...\n");
#endif

    if (!DetachStorageOnly && !HuaweiMode ) {
	    if (show_progress) printf("Setting up communication with device\n");
        ret = usb_claim_interface(devh, 0);
		if (ret != 0) {
		    if (show_progress) fprintf(stderr, "Error: could not claim interface (error %d). Can't communicate. Aborting\n\n", ret);
		    exit(1);
        }
		ret = usb_clear_halt(devh, MessageEndpoint);

/* If you still have problems try with the following line uncommented */
//		ret = usb_clear_halt(devh, ResponseEndpoint);

        ret = usb_set_altinterface(devh, 0);
		if (ret != 0) {
		    if (show_progress) fprintf(stderr, "Error: could not set alt interface (error %d). Aborting\n\n", ret);
		    exit(1);
        }

		if (!MessageEndpoint) {
		    if (show_progress) fprintf(stderr, "Error: no MessageEndpoint given. Can't send message. Aborting\n");
		    exit(1);
		}

		if (strlen(MessageContent) % 2 != 0) {
		    if (show_progress) fprintf(stderr, "Error: MessageContent hex string has uneven length. Aborting\n\n");
		    exit(1);
		}

	    message_length = strlen(MessageContent) / 2;
		if (!message_length) {
		    if (show_progress) fprintf(stderr, "Error: no MessageContent given. Can't send message. Aborting\n\n", MessageContent);
		    exit(1);
		}
		
		if ( hexstr2bin(MessageContent,ByteString,message_length) == -1) {
		    if (show_progress) fprintf(stderr, "Error: MessageContent: %s\n is not a hex string. Aborting\n\n", MessageContent);
		    exit(1);
		}

		if (show_progress) printf("Trying to send the message\n");
	    write_bulk(MessageEndpoint, ByteString, message_length);

		if (NeedResponse) {
		    if (!ResponseEndpoint) {
				if (show_progress) fprintf(stderr, "Error: No ResponseEndpoint given. Skipping response reading\n");
		    } else {
				if (show_progress) printf("Reading the response\n");
				read_bulk(ResponseEndpoint, ByteString, LINE_DIM/2);
		    }
		}

/* you might try this again if device still does not switch */

//		usb_clear_halt(devh, MessageEndpoint);

/* or one of these: */

//		usb_reset(devh); /* ignore following error messages */
//		usb_resetep(devh, MessageEndpoint); /* marked as deprecated in libusb docs */

    }	
	
	if ( HuaweiMode ) {
		ret = usb_control_msg(devh, USB_TYPE_STANDARD + USB_RECIP_DEVICE, USB_REQ_SET_FEATURE, 00000001, 0, buf, 0, 1000);
		if (ret != 0) {
			if (show_progress) fprintf(stderr, "Error: sending Huawei control message failed (error %d). Aborting\n\n", ret);
		    exit(1);
		} else
			if (show_progress) printf(" OK, Huawei control message successfully sent.\n");
	}

    if (show_progress) printf("-> See /proc/bus/usb/devices (or call lsusb) for changes. Bye\n\n");

    if (!DetachStorageOnly && !HuaweiMode) {
        ret = usb_release_interface(devh, 0);
		if (ret != 0)
			if (show_progress) fprintf(stderr, "Error: releasing interface failed (error %d). Trying to continue\n", ret);
    }

    ret = usb_close(devh);
	if (ret != 0) {
		if (show_progress) fprintf(stderr, "Error: sending Huawei control message failed (error %d). Aborting\n\n", ret);
	    exit(1);
	}

    return 0;
}

int write_bulk(int endpoint, char *message, int length) {
    int ret;
    ret = usb_bulk_write(devh, endpoint, message, length, 1000);
    if (ret >= 0 ) {
		if (show_progress) printf(" OK, message successfully sent.\n");
    } else {
		if (show_progress) printf(" Sending the message returned error %d, trying to continue ...\n", ret);
	}
	return ret;
}

int read_bulk(int endpoint, char *buffer, int length) {
    int ret;
    ret = usb_bulk_read(devh, endpoint, buffer, length, 1000);
    if (ret >= 0 ) {
		if (show_progress) printf(" OK, reading the response was successful.\n");
	} else {
		if (show_progress) printf(" Reading the response returned error %d, trying to continue ...\n", ret);
	}
	return ret;
}

void release_usb_device(int dummy) {
    int ret;
    if (show_progress) printf("Program cancelled by system. Bye\n\n");
    ret = usb_release_interface(devh, 0);
    if (!ret)
		if (show_progress) fprintf(stderr, "Error: failed to release interface: %d\n", ret);
    usb_close(devh);
    if (!ret)
		if (show_progress) fprintf(stderr, "Error: failed to close interface: %d\n", ret);
    if (show_progress) printf("\n");
    exit(1);
}


struct usb_device* search_devices( int *numFound, int vendor, int product, int targetClass) {
    struct usb_bus *bus;
	int devClass;
    struct usb_device* right_dev = NULL;
    
	*numFound = 0;
    for (bus = usb_get_busses(); bus; bus = bus->next) {
		struct usb_device *dev;
		for (dev = bus->devices; dev; dev = dev->next) {
		    if (dev->descriptor.idVendor == vendor && dev->descriptor.idProduct == product) {
				(*numFound)++;
				devClass = dev->descriptor.bDeviceClass;
				if (devClass == 0)
					devClass = dev->config[0].interface[0].altsetting[0].bInterfaceClass;
				if (devClass != targetClass)
					right_dev = dev;
			}
    	}
	}
    return right_dev;
}


// the parameter parsing stuff

char* ReadParseParam(const char* FileName, char *VariableName) {
	static char Str[LINE_DIM];
	char *VarName, *Comment=NULL, *Equal=NULL;
	char *FirstQuote, *LastQuote, *P1, *P2;
	int Line=0, Len=0, Pos=0;
	FILE *file=fopen(FileName, "r");
	
	if (file==NULL) {
		if (show_progress) fprintf(stderr, "Error: Could not find file %s\n\n", FileName);
		exit(1);
	}

	while (fgets(Str, LINE_DIM-1, file) != NULL) {
		Line++;
		Len=strlen(Str);
		if (Len==0) goto Next;
		if (Str[Len-1]=='\n' or Str[Len-1]=='\r') Str[--Len]='\0';
		Equal = strchr (Str, '=');			// search for equal sign
		Pos = strcspn (Str, ";#!");			// search for comment
		Comment = (Pos==Len) ? NULL : Str+Pos;
		if (Equal==NULL or ( Comment!=NULL and Comment<=Equal)) goto Next;	// Only comment
		*Equal++ = '\0';
		if (Comment!=NULL) *Comment='\0';

		// String
		FirstQuote=strchr (Equal, '"');		// search for double quote char
		LastQuote=strrchr (Equal, '"');
		if (FirstQuote!=NULL) {
			if (LastQuote==NULL) {
				if (show_progress) fprintf(stderr, "Error reading parameter file %s line %d - Missing end quote.\n", FileName, Line);
				goto Next;
			}
			*FirstQuote=*LastQuote='\0';
			Equal=FirstQuote+1;
		}
		
		// removes leading/trailing spaces
		Pos=strspn (Str, " \t");
		if (Pos==strlen(Str)) {
			if (show_progress) fprintf(stderr, "Error reading parameter file %s line %d - Missing variable name.\n", FileName, Line);
			goto Next;		// No function name
		}
		while ((P1=strrchr(Str, ' '))!=NULL or (P2=strrchr(Str, '\t'))!=NULL)
			if (P1!=NULL) *P1='\0';
			else if (P2!=NULL) *P2='\0';
		VarName=Str+Pos;
		//while (strspn(VarName, " \t")==strlen(VarName)) VarName++;

		Pos=strspn (Equal, " \t");
		if (Pos==strlen(Equal)) {
			if (show_progress) fprintf(stderr, "Error reading parameter file %s line %d - Missing value.\n", FileName, Line);
			goto Next;		// No function name
		}
		Equal+=Pos;

//		printf("%s=%s\n", VarName, Equal);
		if (strcmp(VarName, VariableName)==0) {		// Found it
			fclose(file);
			return Equal;
		}
		Next:;
	}
	
	// not found
//	fprintf(stderr, "Error reading parameter file %s - Variable %s not found.", 
//				FileName, VariableName);
	fclose(file);
	return NULL;
}

int hex2num(char c)
{
    if (c >= '0' && c <= '9')
	return c - '0';
    if (c >= 'a' && c <= 'f')
	return c - 'a' + 10;
    if (c >= 'A' && c <= 'F')
	return c - 'A' + 10;
    return -1;
}


int hex2byte(const char *hex)
{
    int a, b;
    a = hex2num(*hex++);
    if (a < 0)
	return -1;
    b = hex2num(*hex++);
    if (b < 0)
	return -1;
    return (a << 4) | b;
}

int hexstr2bin(const char *hex, char *buf, int len)
{
    int i;
    int a;
    const char *ipos = hex;
    char *opos = buf;
//    printf("Debug: hexstr2bin bytestring is ");

    for (i = 0; i < len; i++) {
	a = hex2byte(ipos);
//        printf("%02X", a);
	if (a < 0)
	    return -1;
	*opos++ = a;
	ipos += 2;
    }
//    printf(" \n");
    return 0;
}
