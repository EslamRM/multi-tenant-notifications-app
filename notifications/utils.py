from .elasticsearch_utils import create_index


def create_index_for_tenant(schema_name):
    """
    Create an Elasticsearch index for a tenant.
    """
    index_name = f"{schema_name}_notifications"
    mapping = {
        "mappings": {
            "properties": {
                "message": {"type": "text"},
                "created_at": {"type": "date"},
                "read": {"type": "boolean"},
            }
        }
    }
    create_index(index_name, mapping)
