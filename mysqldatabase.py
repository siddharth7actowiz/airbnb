import json
import mysql.connector

# JSON file path
json_file = "D:\\Siddharth\\Aribnb\\pythonProject\\AIRBNB_VALIDATEDFILE_2026_02_23.json"

# Load JSON
def load_validated_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

json_data = load_validated_json(json_file)

# Database connection
con = mysql.connector.connect(
    user="root",
    password="actowiz",
    host="localhost",
    port=3306,
    database="json"
)

cursor = con.cursor()

# =====================================================
# Create Single Table
# =====================================================
create_table_sql = """
CREATE TABLE IF NOT EXISTS properties (
    id INT PRIMARY KEY AUTO_INCREMENT,
    property_id BIGINT UNIQUE,
    property_name VARCHAR(255),
    guest_capacity INT,
    property_type VARCHAR(255),
    description TEXT,
    url TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    host_id VARCHAR(255),
    host_name VARCHAR(255),
    host_profile_pic TEXT,
    is_superhost BOOLEAN,
    is_verified BOOLEAN,
    host_rating_count INT,
    host_rating_average DECIMAL(3,2),
    response_rate VARCHAR(100),
    response_time VARCHAR(100),
    star_rating DECIMAL(3,2),
    reviews_count INT,
    amenities JSON,
    house_rules JSON,
    room_images JSON,
    rating_info JSON,
    security_concerns JSON,
    host_highlights JSON,
    co_hosts JSON
);
"""
cursor.execute(create_table_sql)

# =====================================================
# Insert Query
# =====================================================
insert_sql = """
INSERT INTO properties (
    property_id,
    property_name,
    guest_capacity,
    property_type,
    description,
    url,
    city,
    state,
    country,
    host_id,
    host_name,
    host_profile_pic,
    is_superhost,
    is_verified,
    host_rating_count,
    host_rating_average,
    response_rate,
    response_time,
    star_rating,
    reviews_count,
    amenities,
    house_rules,
    room_images,
    rating_info,
    security_concerns,
    host_highlights,
    co_hosts
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

values = (
    json_data.get("Property_id"),
    json_data.get("Property_name"),
    json_data.get("Guest_capacity"),
    json_data.get("Property_type"),
    json_data.get("Description"),
    json_data.get("Url"),
    json_data.get("Address_info", {}).get("City"),
    json_data.get("Address_info", {}).get("State"),
    json_data.get("Address_info", {}).get("Country"),
    json_data.get("Host", {}).get("Host_id"),
    json_data.get("Host", {}).get("Host_name"),
    json_data.get("Host", {}).get("Profile_pic"),
    json_data.get("Host", {}).get("Is_superhost"),
    json_data.get("Host", {}).get("Is_verified"),
    json_data.get("Host", {}).get("Rating_count"),
    json_data.get("Host", {}).get("Rating_average"),
    json_data.get("Host", {}).get("Response_rate"),
    json_data.get("Host", {}).get("Response_time"),
    json_data.get("Star_rating"),
    json_data.get("Reviews_count"),
    json.dumps(json_data.get("Amenities")),
    json.dumps(json_data.get("Houserules")),
    json.dumps(json_data.get("Room_info")),
    json.dumps(json_data.get("Rating_info")),
    json.dumps(json_data.get("Security_concerns")),
    json.dumps(json_data.get("Host", {}).get("HighLights")),
    json.dumps(json_data.get("Host", {}).get("Co_host"))
)

cursor.execute(insert_sql, values)
print(cursor.rowcount, "property inserted.")

con.commit()
cursor.close()
con.close()

