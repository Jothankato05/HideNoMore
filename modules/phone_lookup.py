import phonenumbers
from phonenumbers import geocoder, carrier

def lookup(number):
    try:
        parsed_number = phonenumbers.parse(number)
        country = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")
        print(f"Country: {country}")
        print(f"Carrier: {carrier_name}")
    except phonenumbers.phonenumberutil.NumberParseException:
        print("Invalid phone number format")
