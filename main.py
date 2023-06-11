import db_config, functions

def main():
	"""
		Automation script extracting data from a database in a specified time range
		and saving them to new files locally (for the time being)
	"""
	dt10pm = dt.datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
	dt12pm = dt.datetime.now().replace(hour=13, minute=59, second=59, microsecond=0)
	while True:
		now = dt.datetime.now()
		if now >= dt10pm and now <= dt12pm:
			conn = functions.connectDb(db_config.CONNECTION_INFO)
			functions.makeMtrdata(conn)
			functions.makeMtrl(conn)
			functions.makeTrdr(conn)
			print("Success.")
			time.sleep(60*240)
		else:
			print("Sleeping...")
			time.sleep(2)


if __name__ == '__main__':
	main()