import requests
import os
from airflow.hooks.base_hook import BaseHook

MOVIELENS_HOST = os.environ.get('MOVIELENS_HOST', 'movielens')
MOVIELENS_PORT = os.environ.get('MOVIELENS_PORT', '5000')
MOVIELENS_USER = os.environ.get('MOVIELENS_USER', 'airflow')
MOVIELENS_PASSWORD = os.environ.get('MOVIELENS_PASSWORD', 'airflow')

class MovielensHook(BaseHook):
    def __init__(self, conn_id):
        super().__init__()
        self._conn_id = conn_id
        self._session = None 
        self._base_url = None 

    def _get_conn(self):
        if self._session is None:
            config = self.get_connection(self._conn_id)
            session = requests.Session()
            schema = config.schema or self.DEFAULT_SCHEMA
            host = config.host or MOVIELENS_HOST
            port = config.port or MOVIELENS_PORT

            self._base_url = f"{schema}://{host}:{port}"

            if config.login:
                session.auth = (config.login, config.password)

            self._session = session

        return self._session, self._base_url
    

    def get_ratings(self, start_date=None, end_date=None, batch_size=100):
        yield from self._get_with_pagination(
            endpoint="/ratings",
            params={"start_date": start_date, "end_date": end_date}, 
            batch_size=batch_size
        )

    def _get_with_pagination(self, endpoint, params, batch_size=100):
        session, base_url = self._get_conn()
        url = f"{base_url}{endpoint}"
        offset = 0
        total = None
        while total is None or offset < total:
            response = session.get(url, params={**params, 'offset': offset, 'limit': batch_size})
            response.raise_for_status()
            response_json = response.json()

            yield from response_json['result']

            offset += batch_size
            total = response_json['total']

    def close(self):
        if self._session:
            self._session.close()
            self._session = None
    