"""
-- Created by: Ashok Kumar Pant
-- Created on: 8/14/23
"""
from datetime import datetime
from traceback import print_exc

import elasticsearch as es
import elasticsearch.helpers as es_helpers

if __name__ == '__main__':
    host = 'http://elastic:changeme@localhost:9200'
    try:
        es_client: es.Elasticsearch = es.Elasticsearch(
            hosts=[host])
        print(es_client.info())
        actions = [
            {'_index': "text-index",
             '_op_type': 'index',
             '@timestamp': datetime.now().isoformat(),
             'level': "DEBUG",
             'content': "This is a test message"
             }
        ]
        es_helpers.bulk(es_client, actions, stats_only=True)
    except es.exceptions.ConnectionError:
        print_exc()
