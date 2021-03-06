#!/usr/bin/env python
from __future__ import print_function
import argparse
import binascii
import os
import sys
from bluepy import btle
import datetime
import pprint as pp


if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'

bluetooth_devices = {}
bd_list = {}
bd_list2 = {}

Mac_rssi={}


def dump_services(dev):
    services = sorted(dev.services, key=lambda s: s.hndStart)
    for s in services:
        print("\t%04x: %s" % (s.hndStart, s))
        if s.hndStart == s.hndEnd:
            continue
        chars = s.getCharacteristics()
        for i, c in enumerate(chars):
            props = c.propertiesToString()
            h = c.getHandle()
            if 'READ' in props:
                val = c.read()
                if c.uuid == btle.AssignedNumbers.device_name:
                    string = ANSI_CYAN + '\'' + \
                             val.decode('utf-8') + '\'' + ANSI_OFF
                elif c.uuid == btle.AssignedNumbers.device_information:
                    string = repr(val)
                else:
                    string = '<s' + binascii.b2a_hex(val).decode('utf-8') + '>'
            else:
                string = ''
            print("\t%04x:    %-59s %-12s %s" % (h, c, props, string))

            while True:
                h += 1
                if h > s.hndEnd or (i < len(chars) - 1 and h >= chars[i + 1].getHandle() - 1):
                    break
                try:
                    val = dev.readCharacteristic(h)
                    print("\t%04x:     <%s>" %
                          (h, binascii.b2a_hex(val).decode('utf-8')))
                except btle.BTLEException:
                    break


class ScanPrint(btle.DefaultDelegate):

    def __init__(self, opts):
        btle.DefaultDelegate.__init__(self)
        self.opts = opts

    def handleDiscovery(self, dev, isNewDev, isNewData):
        rssi_list=[]
        #print("11111111111111111111111111111111111111111111111111111111111111111111")
        #pp.pprint(bd_list)  
        val=0

        if isNewDev:
            status = "new"
            #for i in range(0,len(self.array)):
                #if
        elif isNewData:
            #if self.opts.new:
                #return
            status = "update"
            #return
        else:
            #if not self.opts.all:
                #return
            status = "old"

        if dev.rssi < self.opts.sensitivity:
            return



        '''print('    Device (%s): %s (%s), %d dBm %s' %
              (status,
               ANSI_WHITE + dev.addr + ANSI_OFF,
               dev.addrType,
               dev.rssi,
               ('(connectable)' if dev.connectable else '(not connectable)'))
              )
        for (sdid, desc, val) in dev.getScanData():
            if sdid in [8, 9]:
                print('\t' + desc + ': \'' + ANSI_CYAN + val + ANSI_OFF + '\'')
            else:
                print('\t' + desc + ': <' + val + '>')
                #manufacturer = (val if 'Manufacturer' in desc else None)'''

        if not dev.scanData:
            print('\t(no data)')


        #rssi_list.append(dev.rssi)



        bluetooth_devices[dev.addr] = \
            {'rssi': dev.rssi,
             'conn': ('connectable' if dev.connectable else 'not connectable'),
             'add_type': dev.addrType,
             #'manufacturer': manufacturer
              }



        #print(bd_list.keys())
        if status=="new" or (dev.addr not in bd_list.keys()):
            rssi_list.append(dev.rssi)
            bd_list[dev.addr] = \
                {
                    'rssi': rssi_list,
                }

        else:
            for i in range(0, len(bd_list[dev.addr]['rssi'])):
                rssi_list.append(bd_list[dev.addr]['rssi'][i])

            #print(str(rssi_list)) 
            rssi_list.append(dev.rssi)
            #print(str(rssi_list)) 

            bd_list[dev.addr] = \
                {
                    'rssi': rssi_list,
                }
        #print("222222222222222222222222222222222222222222222222222222222222222222")
        #pp.pprint(bd_list)    
        #print(str(rssi_list))
        # minRSSI_bd

       # print()


def main():
    ############### my add ###############
    bd_list.clear()
    ######################################

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--hci', action='store', type=int, default=0,
                        help='Interface number for scan')
    parser.add_argument('-t', '--timeout', action='store', type=int, default=0.5,
                        help='Scan delay, 0 for continuous')
    parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128,
                        help='dBm value for filtering far devices')
    parser.add_argument('-d', '--discover', action='store_true',
                        help='Connect and discover service to scanned devices')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Display duplicate adv responses, by default show new + updated')
    parser.add_argument('-n', '--new', action='store_true',
                        help='Display only new adv responses, by default show new + updated')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase output verbosity')
    arg = parser.parse_args(sys.argv[1:])

    btle.Debugging = arg.verbose

    scanner = btle.Scanner(arg.hci).withDelegate(ScanPrint(arg))

   # print(ANSI_RED + "Scanning for devices..." + ANSI_OFF)
    devices = scanner.scan(arg.timeout)



    if arg.discover:
        print(ANSI_RED + "Discovering services..." + ANSI_OFF)

        for d in devices:
            if not d.connectable:
                continue

            dev = btle.Peripheral(d)
            dump_services(dev)
            dev.disconnect()



def RSSI_ave(list_RSSI):
    average = "{0:.2f}".format(sum(list_RSSI) / len(list_RSSI))
    return average

def RSSI_max(list_RSSI):
    maximum=max(list_RSSI)
    return maximum

def RSSI_min(list_RSSI):
    minimum=min(list_RSSI)
    return minimum

def RSSI_ave_min_max(list_RSSI):
    count_min=0
    count_max=0
    maximum = max(list_RSSI)
    minimum = min(list_RSSI)

    for i in range(0, len(list_RSSI)):
        if list_RSSI[i]==maximum and count_max==0:
            idx_max=i
        if list_RSSI[i]==minimum and count_min==0:
            idx_min=i

    del list_RSSI[idx_max]
    del list_RSSI[idx_min]

    average = "{0:.2f}".format(sum(list_RSSI) / len(list_RSSI))
    return average



def ScanScan():
    main()



    return bd_list


#pp.pprint(bd_list)





