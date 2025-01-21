import logging
from pythonjsonlogger import jsonlogger
from elasticsearch import Elasticsearch

# Get Elasticsearch details from environment variables
import os
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "fastapi-logs")

# Configure Elasticsearch client
es_client = Elasticsearch(hosts=[ELASTICSEARCH_HOST])

# Custom Elasticsearch handler
class ElasticSearchHandler(logging.Handler):
    def __init__(self, es_client, index_name):
        super().__init__()
        self.es_client = es_client
        self.index_name = index_name

    def emit(self, record):
        log_entry = self.format(record)
        self.es_client.index(index=self.index_name, body=log_entry)




# Configure logger
def configure_logger():
    logger = logging.getLogger("request_logger")
    logger.setLevel(logging.INFO)

    es_handler = ElasticSearchHandler(es_client, ELASTICSEARCH_INDEX)
    es_handler.setLevel(logging.INFO)

    # JSON formatter
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    es_handler.setFormatter(formatter)

    logger.addHandler(es_handler)
    return logger
