from decimal import Decimal

from aiohttp import web

from payments.account import AccountDoesNotExistsError

from .api import credit_funds
from .api import transfer_funds
from .exceptions import InsufficientFundsError


async def credit_view(request):

    data = await request.post()
    try:
        operation_id = await credit_funds(
            request.app['db'],
            int(data['account_id']),
            Decimal(data['amount'])
        )
    except AccountDoesNotExistsError as ex:
        return web.json_response({'error': ex.msg}, status=404)

    return web.json_response({'operation_id': operation_id}, status=202)


async def transfer_view(request):

    data = await request.post()

    try:
        operation_id = await transfer_funds(
            request.app['db'],
            int(data['sender_id']),
            int(data['recipient_id']),
            Decimal(data['amount'])
        )
    except AccountDoesNotExistsError as ex:
        return web.json_response({'error': ex.msg}, status=404)
    except InsufficientFundsError as ex:
        return web.json_response({'error': ex.msg}, status=422)

    return web.json_response({'operation_id': operation_id}, status=202)
