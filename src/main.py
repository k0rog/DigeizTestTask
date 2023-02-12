from dotenv import load_dotenv
load_dotenv('.env')


from api.app import create_app
from api.config import get_config_class


from flask import current_app
from flask_sqlalchemy import get_debug_queries


if __name__ == '__main__':
    config_class = get_config_class()

    app = create_app(config_class)


    @app.after_request
    def after_request(response):
        for query in get_debug_queries():
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
        return response

    app.run(host='0.0.0.0')
