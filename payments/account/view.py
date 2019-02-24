from aiohttp import web

from .api import account_balance
from .api import create_account
from .exceptions import AccountAlreadyExistsError
from .exceptions import AccountDoesNotExistsError


async def create_view(request):

    data = await request.post()
    try:
        result = await create_account(
            request.app['db'],
            data['first_name'],
            data['last_name'],
            data['city'],
            data['currency']
        )
    except AccountAlreadyExistsError as ex:
        return web.json_response({'error': ex.msg}, status=422)

    return web.json_response({'account_id': result}, status=200)


async def balance_view(request):

    data = request.rel_url.query

    try:
        result = await account_balance(
            request.app['db'],
            int(data['account_id'])
        )
    except AccountDoesNotExistsError as ex:
        return web.json_response({'error': ex.msg}, status=404)

    return web.json_response({'account_balance': str(result)}, status=200)
