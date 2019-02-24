from aiohttp import hdrs
from aiohttp import web
from aiohttp.web import StreamResponse

from payments.account import AccountDoesNotExistsError
from payments.utils import to_csv

from .api import billing_report
from .schema import _input_schema
from .schema import _output_schema


async def report_view(request):

    data = _input_schema.load(request.rel_url.query)[0]

    try:
        rows = await billing_report(
            request.app['db'],
            data['first_name'],
            data['last_name'],
            data.get('begin'),
            data.get('end')
        )
    except AccountDoesNotExistsError as ex:
        return web.json_response({'error': ex.msg}, status=404)

    if data.get('csv'):
        data = to_csv(rows)
        data = data.encode('utf8')

        response = StreamResponse()
        response.content_length = len(data)
        response.content_type = 'text/plain'
        response.headers[hdrs.ACCEPT_RANGES] = 'bytes'

        await response.prepare(request)
        await response.write(data)

        return response

    rows = [_output_schema.dump(r) for r in rows]
    return web.json_response({'rows': rows})
