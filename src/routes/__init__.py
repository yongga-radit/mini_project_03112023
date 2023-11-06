from fastapi import APIRouter
from src.routes import sign_up, sign_in, sign_out

router = APIRouter()

router.add_api_route('/user/sign-up', sign_up.signup,
                     methods=['POST'], tags=['Users'])
# router.add_api_route('/user/sign-in', sign_in.signin,
#                          methods=['POST'], tags=['Users'])
# router.add_api_route('/user/sign-out', sign_out.signout,
#                          methods=['POST'], tags=['Users'])
