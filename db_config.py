DRIVER_NAME = "Driver Name" #Example: SQL SERVER
SERVER_NAME = "Server Name"
DATABASE_NAME = "Database Name"


"""
	--- Connection Info ---
	Driver Should be the driver name.
	Server = SERVER NAME
	Database = Database
	Trust_Connection should be yes
	uid = username
	pwd = password
"""
CONNECTION_INFO = f"""
	DRIVER={{{DRIVER_NAME}}};
	SERVER={SERVER_NAME};
	DATABASE={DATABASE_NAME};
	Trust_Connection=Yes;
	uid=Username;
	pwd=Password;
"""
