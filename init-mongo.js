db.CreateUser(
	{
		user: "gabriel", 
		pwd: "gabriel", 
		roles: [
			{
				role: "userAdminAnyDatabase", 
				db: "admin"
			}
		]
	}
)