import json
from datetime import datetime
from pydantic import  BaseModel , Field
from typing import *


input_data = r"C:\\Users\\HP\\OneDrive\\Desktop\\python\\airbnb\\airbnb_input.json"


# # filename for structured_json
f_name = "AIRBNB_VALIDATEDFILE"
today = datetime.today()
todays_date = datetime.strftime(today, "%Y_%m_%d")
file_name = f"{f_name}_{todays_date}.json"


# function to read json
def load_input_json(input_data):
    # updated read function for binary file
    with open(input_data, "rb") as file:
        binary_file = file.read()
        text_data = binary_file.decode("utf-8")
        python_data = json.loads(text_data)
        return python_data


class security(BaseModel):
    Type:str
    Facility:str


class co_host(BaseModel):
    Co_host_id: str
    Co_host_name: str
    Co_host_profile_pic: str


class Host(BaseModel):
    Host_id: str
    Host_name: str
    Profile_pic: str
    Is_superhost: Optional[bool] = None
    Is_verified: Optional[bool] = None
    Rating_count: Optional[int] = None
    Rating_average: Optional[float] = None
    Hosting_years: Optional[int] = None
    Hosting_months: Optional[int] = None
    Response_rate: Optional[str] = None
    Response_time: Optional[str] = None
    HighLights: Optional[List[str]] = None
    Co_host: Optional[List[co_host]]=None      


class Address(BaseModel):
    City:str
    State:str
    Country:str
class Rooms(BaseModel):
    Id:int
    Title:str
    Img_url:str

class ratings(BaseModel):   
    Category_Name:str
    Rating:float
    Description:str
    
# Main model for airbnb data validation and parsing
class Airbnb_base(BaseModel):
    Property_id: int
    Property_name: str
    Guest_capacity:int
    Property_type:str
    Amenities:List[Dict[str,Any]]
    Houserules:List[str]
    Url: str
    Description:str
    Room_info:List[Rooms]
    Address_info: Address
    Host:Host
    Star_rating:Optional[float]=None
    Reviews_count:Optional[int]=None
    Rating_info:List[ratings]
    Security_concerns:List[security]
    



def parser_validate(raw_json_dict):
    #base_path
    base_path = raw_json_dict.get("niobeClientData", [])[0][1].get("data", {}).get("presentation", {}).get(
        "stayProductDetailPage", {}).get("sections", {})
    #path to seoFeatures dict
    seofeatures=base_path.get("metadata", {}).get("seoFeatures", {})

    # path to embedData dict
    embedData=base_path.get("sections", [])[2].get("section", {}).get("shareSave", {}).get("embedData", {})

    #path to sharingConfig
    sharingConfig=base_path.get("metadata", {}).get("sharingConfig", {})
   
    aminities_path=base_path.get("sections",[])[21].get("section").get("seeAllAmenitiesGroups",[])
   
    #house rules
    houserules_path=base_path.get("sections", [])[1].get("section", {}).get("houseRules", [])
    #rating path
    ratings_path=base_path.get("sections", [])[6].get("section", {}).get("ratings", [])
    #room info path
    room_path=base_path.get("sections", [])[2].get("section", {}).get("mediaItems", [])
    #host   _info_path
    host_info_path=base_path.get("sections", [])[8].get("section", {}).get("cardData", {})    
    #security concerns path
    security_concerns_path=base_path.get("sections", [])[1].get("section", {}).get("safetyAndPropertiesSections", [])[0].get("items", [])
   

    #Address data
    address={
        "City": sharingConfig.get("location"),
        "State": base_path.get("sections",[])[9].get("section", {}).get("breadcrumbs",[])[2].get("title"),
        "Country": base_path.get("sections",[])[9].get("section", {}).get("breadcrumbs",[])[1].get("title") }


    #ratings data
    ratings_info=[]
    
    for rating in ratings_path:
        temp_rating={
            "Category_Name": rating.get("categoryType"),
            "Rating":rating.get("localizedRating"),
            "Description":rating.get("accessibilityLabel")        

        }
        ratings_info.append(temp_rating)



    #romm info data
    room_info=[]
    
    
    for image in room_path:
        temp_dict={
            "Id":image.get("id"),
            "Title":image.get("accessibilityLabel"),
            "Img_url":image.get("baseUrl"),
        }
        
        
        room_info.append(temp_dict)
    
     #houserules data
    houserules=[]
    
    for rules in houserules_path:
        temp_rules={
            "Rules":rules.get("title").strip()
        }
        houserules.append(temp_rules.get("Rules"))
  
    
     #host and cohost data
    cohost=[]
    for co_host in base_path.get("sections",[])[8].get("section",{}).get("cohosts", []):
        cohost_dict={
            "Co_host_id": co_host.get("userId"),
            "Co_host_name": co_host.get("name"),
            "Co_host_profile_pic": co_host.get("profilePictureUrl"),
             
        }
        cohost.append(cohost_dict)

    host_detalis=base_path.get("sections", [])[8].get("section", {}).get("hostDetails",[])
    response_rte=host_detalis[0].strip()
    response_tme=host_detalis[1].strip()
    host_hightlights=[]
    for host_hightlight in base_path.get("sections", [])[8].get("section", {}).get("hostHighlights",[]):
        host_hightlights.append(host_hightlight.get("title"))
    
    
    host_info={
        "Host_id":host_info_path.get("userId"),
        "Host_name":host_info_path.get("name"),
        "Profile_pic":host_info_path.get("profilePictureUrl"),
        "Is_superhost":host_info_path.get("isSuperhost"),
        "Is_verified":host_info_path.get("isVerified"),
        "Rating_count":host_info_path.get("ratingCount"),
        "Rating_average":host_info_path.get("ratingAverage"),
        "Hosting_years": host_info_path.get("timeAsHost",{}).get("years",0),
        "Hosting_months": host_info_path.get("timeAsHost",{}).get("months",0),
        "Response_rate":response_rte,
        "Response_time":response_tme,
        "HighLights":host_hightlights,
        "Co_host":cohost
        
    }

    #amenities data

    amenities=[]
    for amenity in aminities_path:
        temp={
            "Main_Category": amenity.get("title"),
        }
        temp_amenites=[]
        for sub_amenity in amenity.get("amenities",[]):
            
            temp_amenites.append(sub_amenity.get("title"))
            temp["Sub_Category"]=temp_amenites
        amenities.append(temp)
   
 
    #security concerns data
    security_concerns=[]
    for security in security_concerns_path:
        temp_security={
            "Type":security.get("title"),
            "Facility":security.get("subtitle")
                    }
        security_concerns.append(temp_security)


    # VALIDATION and creating model instance
    airbnb_data = Airbnb_base.model_validate({

        "Property_id": embedData.get("id"),
        "Property_name": embedData.get("name"),
        "Guest_capacity": embedData.get("personCapacity"),
        "Property_type":embedData.get("propertyType"),
        "Amenities":amenities,
        "Houserules": houserules,
        "Url": seofeatures.get("canonicalUrl"),
        "Description":base_path.get("sections",[])[20].get("section",{}).get("htmlDescription",{}).get("htmlText"),
        "Room_info": room_info,
        "Address_info": Address(**address),
        "Host": host_info,
        "Star_rating": embedData.get("starRating"),
        "Reviews_count": embedData.get("reviewCount"),
        "Rating_info": ratings_info,
        "Security_concerns":security_concerns
           
    })
    print(airbnb_data)

    # model_dump to create dictonary
    validated_data=Airbnb_base.model_dump(airbnb_data)
    return validated_data


def export_validated_json(validated_json_data):
    with open(file_name,"w",encoding="utf-8") as file:
        json.dump(validated_json_data,file,indent=4,ensure_ascii=False)



#load json
raw_json_dict=load_input_json(input_data)

#validate and create model instance
validated_json_data=parser_validate(raw_json_dict)

#export validated data to json file
export_validated_json(validated_json_data)


