#!/usr/bin/env python
# 
# Philippe Portes February 2017 based on Michael Saunby. April 2013
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import sys
import requests
from bluepy.btle import Scanner, DefaultDelegate

AMP_CO2=0
AMP_PM25=0
AMP_PM10=0
AMP_TVOC=0
AMP_HUM=0
AMP_TEM=0
AMP_IAQ=0
AMP_BATT=0
AMP_CHARG=0
 
class AirMentorProDelegate(DefaultDelegate):
    def __init__(self, bluetooth_adr):
        self.adr = bluetooth_adr
	self.s=requests.Session()
	self.AMP_CO2=0
	self.AMP_PM25=0
	self.AMP_PM10=0
	self.AMP_TVOC=0
	self.AMP_HUM=0
	self.AMP_TEM=0
	self.AMP_IAQ=0
	self.AMP_BATT=0
	self.AMP_CHARG=0
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewdata):
        #print "Notification received #2"
	if dev.addr == self.adr:
	    for scan in dev.getScanData():
		
            	if scan[0] == 0xff: # Proprietary
	            payload = {}
			      
                    if int(scan[2][0:4],16)==0x2221:			      
                        print scan,
			hex_data = scan[2]     
		        #      [TVOC][Temp][Humi][IAQ ]
			#[2221][00b9][1963][332d][0145]			      
                   
			self.AMP_TVOC=int(hex_data[4:8],16)
                   	print "AMP_TVOC",self.AMP_TVOC,

	                self.AMP_TEM=(int(hex_data[8:12],16)-0x11DE)/100.0
		   	print "AMP_TEM: ",self.AMP_TEM,

		   	self.AMP_HUM=(int(hex_data[12:16],16)-0x221B)/100.0  #22210095[1968][392a][0023] 59%
		   	                                                     
		   	                                                     #222100ec[1870][0c2a][0025] 45%
                   	print "AMP_HUM: ",self.AMP_HUM,                      #222100ee[1866][0c2b][0026] 46%
                   	
                   							     #222100f2[1861][0c2d][0026] 48%

 			self.AMP_IAQ=int(hex_data[16:],16)
                        print "AMP_IAQ",self.AMP_IAQ

		    	try:
	                   requests.get("http://localhost/airmentorpro2.php?Action=set&CO2="+str(self.AMP_CO2)+"&PM25="+str(self.AMP_PM25)+"&PM10="+str(self.AMP_PM10)+"&TEM="+str(self.AMP_TEM)+"&HUM="+str(self.AMP_HUM)+"&TVOC="+str(self.AMP_TVOC)+"&IAQ="+str(self.AMP_IAQ)+"&BATT="+str(self.AMP_BATT), data=payload) 
			except:
                       	   print "Couldn't send request..."
                                                   
		    else:
			if int(scan[2][0:4],16)==0x2121:
			    hex_data = scan[2]      
			    #       [CO2 ][PM25][PM10]
			    # [2121][2710][0003][0003]0000
                            print scan,
			    self.AMP_CO2=int(hex_data[4:8],16)
		            print "AMP_CO2",self.AMP_CO2,

	                    self.AMP_PM25=int(hex_data[8:12],16)
	                    print "AMP_PM25",self.AMP_PM25,

	                    self.AMP_PM10=int(hex_data[12:16],16)
	                    print "AMP_PM10",self.AMP_PM10
            
                            #AMP_BATT=int(hex_data[16],16)
                            #print "self.AMP_BATT",self.AMP_BATT,
                            try:
	                        requests.get("http://localhost/airmentorpro2.php?Action=set&CO2="+str(self.AMP_CO2)+"&PM25="+str(self.AMP_PM25)+"&PM10="+str(self.AMP_PM10)+"&TEM="+str(self.AMP_TEM)+"&HUM="+str(self.AMP_HUM)+"&TVOC="+str(self.AMP_TVOC)+"&IAQ="+str(self.AMP_IAQ)+"&BATT="+str(self.AMP_BATT), data=payload) 
			    except:
                       	        print "Couldn't send request..."
                #else:
                #    print "[",scan[0],":", scan[2], "]"			 


def main():
    global datalog
    global barometer
    
    bluetooth_adr = sys.argv[1]

    print  bluetooth_adr

    while True:
        try:   
            # BTLE UUSB is on hci1, so pass 1 to Scanner
            scanner = Scanner(1).withDelegate(AirMentorProDelegate(bluetooth_adr))

            

   	    while(1):
	        scanner.start()
	        scanner.process(1)
	        scanner.stop()
                

        except:
            pass

if __name__ == "__main__":
    main()