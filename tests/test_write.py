import logging
from time import sleep

import requests

from src.python_elasticsearch_logging import ElasticHandler


def test_write_text(elastic_host, debug_logger):
    index = 'test-index'
    content = 'test exception'

    handler = ElasticHandler(
        elastic_host, index, level=logging.DEBUG, flush_period=0.5)

    test_logger = debug_logger(handler)
    test_logger.exception(content)

    sleep(3)  # Wait for batch + send latency + new index creation

    raw_result = requests.get(f'{elastic_host}/{index}/_search')
    json_result = raw_result.json()

    assert json_result['hits']['total']['value'] == 1

    message_obj = json_result['hits']['hits'][0]['_source']
    assert message_obj['level'] == logging._levelToName[logging.ERROR]
    assert message_obj['content'] == content


def test_write_object(elastic_host, debug_logger):
    index = 'test-index'
    content = {
        'key1': 'value1',
        'key2': 'value2'
    }

    handler = ElasticHandler(
        elastic_host, index, level=logging.DEBUG, flush_period=0.5)

    test_logger = debug_logger(handler)
    test_logger.warning(content)

    sleep(3)  # Wait for batch + send latency + new index creation

    raw_result = requests.get(f'{elastic_host}/{index}/_search')
    json_result = raw_result.json()

    assert json_result['hits']['total']['value'] == 1

    message_obj = json_result['hits']['hits'][0]['_source']
    assert message_obj['level'] == logging._levelToName[logging.WARNING]
    assert message_obj['content'] == content
