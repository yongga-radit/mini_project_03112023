from fastapi import APIRouter, Depends
from pydantic import BaseModel
import requests
from src.utils.encryption import validate_token, encode_data


class RegisterData(BaseModel):
    credentials: str


async def encrypt_data(data: RegisterData):
    return encode_data(data)


async def decrypt_data(payload=Depends(validate_token)):
    return payload


async def request_api():
    url = "https://stag-cms.bolehbelajar.com/index.php/wp-json/wp/v2/pages?status=publish"
    header = {
        'Authorization': 'Basic YWRtaW5fY21zOndid1YgNzlucCBFeTRKIFJBVFQgMWdWQyBkeFFH'
    }

    response = requests.get(
        "GET",
        url,
        headers=header,
        data={}
    )

    return response.json()