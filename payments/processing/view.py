from aiohttp import web

from payments.operation import OperationDoesNotExists
from payments.operation import OperationInconsistent

from .api import process_credit_operation
from .api import process_transfer_operation
from .api import send_to_processing


async def process_view(request):

    data = await request.post()

    try:
        history_id = await send_to_processing(
            request.app['db'],
            int(data['operation_id'])
        )
    except OperationDoesNotExists as ex:
        return web.json_response({'error': ex.msg}, status=404)

    return web.json_response({'history_id': history_id}, status=202)


async def process_credit_view(request):

    data = await request.post()

    try:
        operation_status = await process_credit_operation(
            request.app['db'],
            int(data['operation_id'])
        )
    except OperationDoesNotExists as ex:
        return web.json_response({'error': ex.msg}, status=404)
    except OperationInconsistent as ex:
        return web.json_response({'error': ex.msg}, status=422)

    return web.json_response({'status': operation_status}, status=200)


async def process_transfer_view(request):

    data = await request.post()

    try:
        operation_status = await process_transfer_operation(
            request.app['db'],
            int(data['operation_id'])
        )
    except OperationDoesNotExists as ex:
        return web.json_response({'error': ex.msg}, status=404)
    except OperationInconsistent as ex:
        return web.json_response({'error': ex.msg}, status=422)

    return web.json_response({'status': operation_status})
