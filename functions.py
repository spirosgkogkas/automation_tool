import pyodbc
import csv
import datetime as dt
import time
import paramiko
from base64 import decodebytes

#Headers
HEADER_010 = ["Κωδικός", "Βασικός Κωδικός", "Περιγραφή", "Κωδικός Προμηθευτή", "Κωδικοποίηση Προμηθευτή"]
HEADER_020 = ["Κωδικός", "Ποσότητα Αποθέματος"]
HEADER_030 = ["Κωδικός Πελάτη", "Επωνυμία Πελάτη", "ΑΦΜ Πελάτη", "Πόλη", "Οδός", "Αριθμός", "Νομός", "ΤΚ", "Δραστηριότητα"]

def connectDb(connection_info: str):
	"""
		connectDb returns a connection.
		connection_info -> str
		Multiline String with the information needed for the connection
		(DRIVER=DRIVER_NAME, SERVER=SERVER_NAME, DATABASE=DATABASE_NAME, UID=USERNAME, PWD=PASSWORD)
	"""
	conn = pyodbc.connect(connection_info)
	return conn

def makeMtrl(conn):
	"""
		The makeMtrl function fetches the necessary data for the first file and stores them in a new file
		 with a name consisting of the header information and the time of file creation.
	"""
	try:
		cursor = conn.cursor()
		cursor.execute("""
		SELECT Code,Code,Name,Acnmsk9,Code2 FROM dbo.MTRL
		WHERE SODTYPE = 51;
		""")

		t = dt.datetime.now().strftime("%Y%m%d%H%M")
		with open(f"010_801118179_{t}_094135871.csv", "w", encoding="utf-8", newline="") as f:
			writer = csv.writer(f)
			writer.writerow(HEADER_010)
			writer.writerows(cursor.fetchall())
	except Exception as e:
		print(e)

def makeMtrdata(conn):

	""" 
		This function is responsible for creating the second file (0_20)
	"""
	try:
		cursor = conn.cursor()
		cursor.execute("""SELECT MTRL.CODE, QTY1 FROM dbo.MTRDATA
						  INNER JOIN dbo.MTRL
						  ON MTRL.MTRL = MTRDATA.MTRL
						  WHERE mtrl.SODTYPE = 51
						  ORDER BY MTRL.CODE
		""")

		t = dt.datetime.now().strftime("%Y%m%d%H%M")
		with open(f"020_801118179_{t}_094135871.csv", "w", encoding="utf-8", newline="") as f:
			writer = csv.writer(f)
			writer.writerow(HEADER_020)
			writer.writerows(cursor.fetchall())
	except Exception as e:
		print(e)

def makeTrdr(conn):
	"""
		This function is responsible for creating the third file (0_30)
	"""
	try:
		cursor = conn.cursor()
		cursor.execute("""SELECT TRDR.CODE,TRDR.NAME,TRDR.AFM,TRDR.CITY,TRDR.ADDRESS,TRDR.DISTRICT1,NULL,TRDR.ZIP,TRDR.JOBTYPETRD, TRDBRANCH.CODE as 'Κωδικός Υποκαταταστήματος'
						  FROM dbo.TRDR
					      INNER JOIN dbo.TRDBRANCH
						  ON TRDR.TRDR = TRDBRANCH.TRDR
						  WHERE (TRDR.SODTYPE = 12 OR TRDR.SODTYPE = 13);""")

		t = dt.datetime.now().strftime("%Y%m%d%H%M")
		with open(f"030_801118179_{t}_094135871.csv", "w", encoding="utf-8", newline="") as f:
			writer = csv.writer(f)
			writer.writerow(HEADER_030)
			writer.writerows(cursor.fetchall())
	except Exception as e:
		print(e)

def connectSFTP(username, password=None, server_ip=None, public_key=None):
	"""
		connectSFTP will get used to estabilish secure connection with the server and upload all the files
		in an upcoming update.
		Here is only the part of the connection to the server for testing purposes with paramiko.
	"""
	client = paramiko.SSHClient()
	if public_key:
		public_key = paramiko.RSAKey(data=decodebytes(public_key))
		if server_ip:
			client.get_host_keys().add(server_ip, "ssh-rsa", public_key)
		else:
			input("Enter Domain/IP: ")
			client.get_host_keys().add(server_ip, "ssh-rsa", public_key)
		if password:
			client.connect(server_ip, username=username, passwd=password, key_filename="./id_rsa")
		else:
			client.connect(server_ip, username=username, key_filename="./id_rsa")

		sftp_client = client.open_sftp()
		sftp_client.chdir(".")
		print(sftp_client.getcwd())
