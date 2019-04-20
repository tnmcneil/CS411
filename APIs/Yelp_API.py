'''
pip install yelpapi
'''
import config
from yelpapi import YelpAPI
yelp_api = YelpAPI(config.YELP_API_TOKEN)

def get_reviews_of_business(name,address1,city,state,country):
    response = yelp_api.business_match_query(name=name,
                                            address1=address1,
                                            city=city,
                                            state=state,
                                            country=country)

    response = yelp_api.reviews_query(id=response['businesses'][0]['alias'])
    return (response)

def get_reviews_of_business_by_phone(phone): #"+16173545433"
    response = yelp_api.phone_search_query(phone="+16173545433")
    response = yelp_api.reviews_query(id=response['businesses'][0]['alias'])
    return (response)

