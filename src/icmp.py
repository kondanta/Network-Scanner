import os
import sys
try:
	import nmap
	from scapy.all import *
except ModuleNotFoundError:
    print('Required modules are not found. Please check the ReadMe file for requirements.')
    sys.exit(0)

conf.L3socket = L3RawSocket
TIMEOUT = 2
conf.verb = 0

def icmp_ping(ip1='192.168.1.1', ip2='192.168.1.255'):
	"""
	Takes two IP addresses as a paramters to find pinging range.
	"""
	try:
		i1 = ip1.split(".")
		i2 = ip2.split(".")
		ip = i1[:3]
		ip_o = ".".join(ip) + "."
		for ip in range(int(i1[3]), int(i2[3])+1): # some bs
			packet = IP(dst=ip_o + str(ip), ttl=20)/ICMP()
			reply = sr1(packet, timeout=TIMEOUT)
			if not (reply is None):
				f = open('icmp.dat', 'a')
				f.write(reply.src + '\n')
				f.close()
				x = reply.src + " is online"
				print(x)
			else:
				x = "%s is offline" % packet[IP].dst
				print(x)
	except OSError:
		print("Check the given ips")
	

def port_identification():
	"""
	Uses nmap to scan alive hosts ports.
	For ip's icmp.dat file is required.
	"""
	lst = list()
	nm = nmap.PortScanner()

	for ips in open("icmp.dat", "r").readlines():
		lst.append(ips.strip())
	try:
		for ip in lst:
			a = nm.scan(ip, arguments="-sT -d -d")
			b = (a['scan'][ip]['tcp'])

			f = open('ports.dat', 'a')
			f.write(ip+", ")

			for key, values in b.items():
				print(key)
				x = "Protocol: TCP, Port Number: %s, State: %s, Reason: %s, Service-name: %s. " %\
				(key, values['state'], values['reason'], values['name'])
				f.write(x)

			c = nm.scan(ip, arguments="-sU -d -d")
			d = (c['scan'][ip]['udp'])
			for key, values in d.items():
				print(key)
				x = "Protocol: UDP, Port Number: %s, State: %s, Reason: %s, Service-name: %s. " %\
				(key, values['state'], values['reason'], values['name'])
				f.write(x)

			f.write('\n')
			f.close()
	except KeyError:
		print('Network Error!')
		pass

def open_port_identification():
	"""
	Find the open ports of the ip addresses in ports.dat file.
	"""
	lst = list()
	ip_table = list()
	nm = nmap.PortScanner()

	for ips in open("ports.dat", "r").readlines():
		lst.append(ips.strip())
 	
 	# Separating the ips.
	for item in lst:
		item = item.split(",")
		ip_table.append(item[0])

	# since nmap library's outputs similar to the json format
	# I couldnt find a good way to implement but using 2 loops.
	try:
		for ip in ip_table:
			a = nm.scan(ip)
			b = (a['scan'][ip]['tcp'])
			print(a)
			f = open('open_ports.dat', 'a')
			f.write(ip+", ")
			for key, values in b.items():
				x = "Port Number: %s, State: %s, Reason: %s, Service-name: %s, Product: %s." %\
				(key, values['state'], values['reason'], values['name'], values['product'])
				
				f.write(x)
			f.write('\n')
			f.close()
	except KeyError:
		print("Could not find any ports to scan. Please be sure that your network allows scanning")
		pass


import sys
def os_ident():
	if sys.platform == 'win32':
		print('This function does not work on windows')
		return
	else:
		lst = list()
		ip_table = list()
		os_list = list()

		nm = nmap.PortScanner()
		cnt = 0

		for ips in open("open_ports.dat", "r").readlines():
			lst.append(ips.strip())

		for item in lst:
			item = item.split(",")
			ip_table.append(item[0])

		print(ip_table)

		try:

			for ip in ip_table:

				nm.scan(ip, arguments="-O")

				a = nm[ip]['osmatch']
				b = a[0]['name']
				print(b)
				os_list.append(b)

			print(os_list)

		except IndexError:
			print("Couldn't able to find the OS. Please check the open ports and ips.")

		f = open('os_ident.dat', 'a')
				
		for i in os_list:

			f.write(ip_table[cnt]+" ")
			f.write(i+"\n")
			cnt += 1

		f.close()


  