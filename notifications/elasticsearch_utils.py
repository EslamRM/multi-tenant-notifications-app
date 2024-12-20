from elasticsearch import Elasticsearch
from django.conf import settings

es_client = Elasticsearch(settings.ELASTICSEARCH_HOST)


def create_index(index_name, mapping=None):
    if not es_client.indices.exists(index=index_name):
        body = {"mappings": mapping} if mapping else {}
        es_client.indices.create(index=index_name, body=body)


def delete_index(index_name):
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)


def index_document(index_name, doc_id, document):
    print(f"Indexing Document: {doc_id} in Index: {index_name} with Data: {document}")
    es_client.index(index=index_name, id=doc_id, body=document)


def delete_document(index_name, doc_id):
    es_client.delete(index=index_name, id=doc_id)


def search_index(index_name, query):
    return es_client.search(index=index_name, body=query)


def get_tenant_index(schema_name):
    return f"{schema_name}_notifications"
