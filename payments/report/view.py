from aiohttp import web

from .api import billing_report
from .schema import report_schema


async def report_view(request):

    data = request.rel_url.query

    rows = await billing_report(
        request.app['db'],
        data['first_name'],
        data['last_name'],
        data['begin'],
        data['end']
    )

    rows = [report_schema.dump(r) for r in rows]

    return web.json_response({'rows': rows})
