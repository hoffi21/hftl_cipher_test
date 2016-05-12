# coding: utf-8

# IMPORTS
import sys
import socket
import ssl
import timeit
import xlsxwriter

# Global Vars
Host = "www.google.com"
Port = 443
k = 1
n = 0
myList = []
HOST = socket.getaddrinfo(Host, Port)[0][4][0]

# liefert eine Liste zurück
# 5-Tupel (family, socktype, protocol, canonname, sockaddr)
# socktype 2 = SOCK_DGRAM; socktype 1 = SOCK_STREAM
# protocol 6 = TCP; protocol 17 = UDP
# canonname ist nahezu immer leer
# sockaddr liefert eine Socketadresse zurück => bei IPv4 2-Tupel (IP, Port);
# bei IPv6 4-Tupel (IP, Port, flow info , scope id )
#
# 1. [] gibt an welches Tupel (wenn mehrere zurückkommen) man nimmt
# 2. [] gibt an welches Element des Tupels man wählt
# 3. [] falls dieses Element ebenfalls eine Liste ist, gibt man welches Element
# dieser Liste man nimmt => in diesem Fall bekommt man die IP raus

# Asking for cipher
try:
	cipher = raw_input("Cipher? \n")
	myList.append(cipher)
	dec = input("You want another cipher to test? 1 yes, 0 no: \n")
except KeyboardInterrupt:
	print 'Bye.'
	sys.exit()
if dec == 1:
	while dec == 1:
		try:
			cipher = raw_input("Cipher? \n")
			# Element an eine List anhängen
			myList.append(cipher)
			k += 1
			dec = input("You want another cipher to test? 1 yes, 0 no: \n")
		except KeyboardInterrupt:
			print 'Bye.'
			sys.exit()
elif dec != 0 and dec != 1:
	try:
		dec = input("Please insert a valid choice! ")
	except KeyboardInterrupt:
		print 'Bye.'
		sys.exit()
	if dec == 1:
		while dec == 1:
			try:
				cipher = raw_input("Cipher? \n")
				# Element an eine List anhängen
				myList.append(cipher)
				k += 1
				dec = input("You want another cipher to test? 1 yes, 0 no: \n")
			except KeyboardInterrupt:
				print 'Bye.'
				sys.exit()
print(myList)
print(Host, Port, HOST, 'Version: TLS 1.2')

# Create the file
workbook = xlsxwriter.Workbook('ssl_times.xlsx')
for cipher in myList:
	# For each cipher an seperate sheet
	worksheet = workbook.add_worksheet(cipher)
	worksheet.write('A1', 'Beginn in Sekunden')
	worksheet.write('B1', 'Ende in Sekunden')
	worksheet.write('C1', 'Dauer in Sekunden')
	# Create Socket and establish the connection
	i = 1
	j = 1
	while i < 11:
		# 10 connection establishments
		print (str(i)+ '. Durchlauf')
		j += 1
		# stop time before TCP SYN
		time1 = timeit.time.clock()
		# Creating an socket to match the target socket
		# AF_INET = v4 family; AF_INET6 = v6
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# wrap a ssl socket around the standard socket
		try:
			wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2, ciphers=cipher)
			wrappedSocket.connect((HOST, Port))
		except Exception:
			print 'Different TLS versions? Different cipher suites? Non-valid cipher?'
			sys.exit()
		print 'Connection established.'
		# stop time after TCP ACK
		time2 = timeit.time.clock()
		time3 = time2-time1
		# writing the measured times in the xlsx file
		worksheet.write('A'+str(j), str(time1))
		worksheet.write('B'+str(j), str(time2))
		worksheet.write('C'+str(j), str(time3))
		i += 1
		wrappedSocket.close()

# Creating a chart in excel
chart1 = workbook.add_chart({'type': 'column'})
while n < k:
	chart1.add_series({
		'values': '='+str(myList[n])+'!$C$2:$C$11',
		'name': str(myList[n]),
	})
	n += 1

chart1.set_title ({'name': 'Vergleich der Verbindungszeiten'})
chart1.set_x_axis({'name': 'Durchgang'})
chart1.set_y_axis({'name': 'Time in Seconds'})

worksheet.insert_chart('G1', chart1)

# Close the book
workbook.close()
sys.exit()
