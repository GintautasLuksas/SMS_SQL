-- Table: Responsibilities
CREATE TABLE "Responsibilities" (
    "ResponsibilityID"   INTEGER PRIMARY KEY,
    "ResponsibilityName" VARCHAR
);

-- Table: Store
CREATE TABLE "Store" (
    "StoreID"            INTEGER PRIMARY KEY,
    "StoreName"          VARCHAR
);

-- Table: Dry Storage Item
CREATE TABLE "Dry Storage Item" (
    "DryStorageItemID"   INTEGER PRIMARY KEY,
    "Name"               VARCHAR,
    "Amount"             INTEGER,
    "Price"              INTEGER,
    "RecipeItem"         BOOLEAN,
    "Chemical"           BOOLEAN,
    "PackageType"        VARCHAR
);

-- Table: Food Item
CREATE TABLE "Food Item" (
    "FoodItemID"         INTEGER PRIMARY KEY,
    "Name"               VARCHAR,
    "Amount"             INTEGER,
    "Price"              INTEGER,
    "StorageCondition"   VARCHAR,
    "ExpiryDate"         DATE
);

-- Table: Store Manager
CREATE TABLE "Store Manager" (
    "StoreManagerID"     INTEGER PRIMARY KEY,
    "StoreID"            INTEGER,
    "Name"               VARCHAR,
    "Country"            VARCHAR,
    "Email"              VARCHAR,
    "PhoneNumber"        INTEGER,
    "MonthlySalary"      INTEGER,
    "PettyCash"          INTEGER,
    FOREIGN KEY ("StoreID") REFERENCES "Store"("StoreID")
);

-- Table: Manager
CREATE TABLE "Manager" (
    "ManagerID"          INTEGER PRIMARY KEY,
    "Name"               VARCHAR,
    "PhoneNumber"        INTEGER,
    "Country"            VARCHAR,
    "Email"              VARCHAR,
    "MonthlySalary"      INTEGER,
    "ResponsibilityID"   INTEGER,
    "StoreID"            INTEGER,
    FOREIGN KEY ("ResponsibilityID") REFERENCES "Responsibilities"("ResponsibilityID"),
    FOREIGN KEY ("StoreID") REFERENCES "Store"("StoreID")
);

-- Table: SM Responsibilities
CREATE TABLE "SM Responsibilities" (
    "ResponsibilityID"   INTEGER,
    "StoreManagerID"     INTEGER,
    PRIMARY KEY ("ResponsibilityID", "StoreManagerID"),
    FOREIGN KEY ("ResponsibilityID") REFERENCES "Responsibilities"("ResponsibilityID"),
    FOREIGN KEY ("StoreManagerID") REFERENCES "Store Manager"("StoreManagerID")
);

-- Table: StoreDryProduct
CREATE TABLE "StoreDryProduct" (
    "StoreID"            INTEGER,
    "DryStorageID"       INTEGER,
    PRIMARY KEY ("StoreID", "DryStorageID"),
    FOREIGN KEY ("StoreID") REFERENCES "Store"("StoreID"),
    FOREIGN KEY ("DryStorageID") REFERENCES "Dry Storage Item"("DryStorageItemID")
);

-- Table: StoreFoodProduct
CREATE TABLE "StoreFoodProduct" (
    "StoreID"            INTEGER,
    "FoodID"             INTEGER,
    PRIMARY KEY ("StoreID", "FoodID"),
    FOREIGN KEY ("StoreID") REFERENCES "Store"("StoreID"),
    FOREIGN KEY ("FoodID") REFERENCES "Food Item"("FoodItemID")
);

-- Table: Worker
CREATE TABLE "Worker" (
    "WorkerID"           INTEGER PRIMARY KEY,
    "Name"               VARCHAR,
    "PhoneNumber"        INTEGER,
    "Email"              VARCHAR,
    "Country"            VARCHAR,
    "HourlyRate"         INTEGER,
    "AmountWorked"       INTEGER,
    "StoreID"            INTEGER,
    FOREIGN KEY ("StoreID") REFERENCES "Store"("StoreID")
);
