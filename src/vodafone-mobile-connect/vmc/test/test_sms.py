# -*- coding: utf-8 -*-
# Copyright (C) 2006-2007  Vodafone España, S.A.
# Author:  Pablo Martí
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
Unittests for the SIM card

You need to be authenticated before running the test suite
"""

__version__ = "$Rev: 1172 $"

from twisted.trial import unittest

from vmc.common.sms import sms

class TestSMS(unittest.TestCase):
    
    def test_gsm_decoder(self):
        septets = [ord(c) for c in 'hola']
        self.assertEqual(sms.gsm_decoder(septets), 'hola')
    
    def test_7bit_pdu(self):
        smsobj = sms.ShortMessageSubmit('+34606575119', u'hola',
                                        smsc='+34646456456')
        result = '07914346466554F611000B914306565711F90000AA04E8373B0C'
        self.assertEqual(smsobj.get_pdu(), result)
    
    def test_ucs2_pdu(self):
        smsobj = sms.ShortMessageSubmit('+34606575119', u'あ叶葉',
                                        smsc='+34646456456')
        result = '07914346466554F611000B914306565711F90008AA06304253F68449'
        self.assertEqual(smsobj.get_pdu(), result)
    
    def test_malformed_pdu_regression_test(self):
        # ticket #207
        # according to http://smartposition.nl/resources/sms_pdu.html#PDU
        # SMSC#+2782913510
        # Sender:6D721383C7631443
        # TimeStamp:30/10/07 22:46:48
        # TP_PID:03
        # TP_DCS:00
        # TP_DCS-popis:Uncompressed Text
        # class:0
        # Alphabet:Default
        #
        # From Vodacom: You have used more than   86% of the data bundle on 27829266567. Please refer to your monthly bill for final usage and charges.
        # Length:141 
        raise unittest.SkipTest("Not solved yet")
        pdu = '069172281953012410D0D62731387C3641340300700103226484808D46F9BB0DB2BEC9E1F1BBAD0365DF75103A6C2F83EAF33219D47ECBCB203A3AEC068140385B09F43683E8E832881CA68741E2BA9BCC2E83DE6E90EC8693E564365BCD767381A0EC72785E06C9CBE6B21C447F83F2EFBA1CD47EBBE968761E244EB3D920F35B0E32A7DD6136A83E0F9FCBA0B09B0C1AA3C3F27379EE02'
        smsobj = sms.pdu_to_message(pdu)
        
    
    def test_pdu_to_sms(self):
        #pdu = '07911356131313F311000A9260214365870008AA0A0068006F006C00610073'
        #oldsmsobj = smsold.pdu_to_message(pdu)
        #newsmsobj = sms.pdu_to_message(pdu)
        #assert oldsmsobj.text == newsmsobj.get_text()
        #assert oldsmsobj.number == newsmsobj.get_number()
        pass
    
    def test_sms_to_pdu(self):
        #smsoldobj = smsold.ShortMessage('+34606575119', u'hola')
        #smsngobj = sms.ShortMessageSubmit('+34606575119', u'hola')
        #assert smsold.message_to_pdu(smsoldobj) == sms.message_to_pdu(smsngobj)
        pass
