db.createUser(
        {
            user: "biolerplate_mongo_user",
            pwd: "boilerplate_mongo_password",
            roles: [
                {
                    role: "readWrite",
                    db: "boilerplate_mongo_db"
                }
            ]
        }
);