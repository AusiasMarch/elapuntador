from starlette.requests import Request


def get_db(request: Request):
    print(request.state.db)
    return request.state.db
