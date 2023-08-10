db.createUser(
    {
      user: "auction-app",
      pwd: "123qwe",
      roles: [
         { role: "dbOwner", db: "auc" }
      ]
    }
,
    {
        w: "majority",
        wtimeout: 5000
    }
);

db.createCollection("test");
