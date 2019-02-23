from aiohttp import web

from .api import account_balance
from .api import create_account
from .exceptions import AccountAlreadyExists
from .exceptions import AccountDoesNotExists


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
    except AccountAlreadyExists as ex:
        return web.json_response({'error': ex.msg}, status=422)

    return web.json_response({'account_id': result}, status=200)


async def balance_view(request):

    data = request.rel_url.query

    try:
        result = await account_balance(
            request.app['db'],
            int(data['account_id'])
        )
    except AccountDoesNotExists as ex:
        return web.json_response({'error': ex.msg}, status=404)

    return web.json_response({'account_balance': str(result)}, status=200)
