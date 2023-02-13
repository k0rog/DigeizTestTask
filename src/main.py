from flask import current_app
from flask_sqlalchemy import get_debug_queries

from api.app import create_app
from api.config import get_config_class


config_class = get_config_class('../.env')
app = create_app(config_class)


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        current_app.logger.warning(
            'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
            % (query.statement, query.parameters, query.duration,
               query.context))
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
