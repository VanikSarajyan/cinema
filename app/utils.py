from fastapi.responses import RedirectResponse
from starlette import status


def redirect_to(path: str):
    return RedirectResponse(url=path, status_code=status.HTTP_302_FOUND)


def redirect_to_login():
    redirect_response = redirect_to("/users/login-page")
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
