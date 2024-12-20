from rest_framework.response import Response
from rest_framework.views import APIView
from notifications.elasticsearch_utils import search_index, get_tenant_index
from notifications.serializers import NotificationSearchSerializer
from django_tenants.utils import schema_context
from django.db import connection
import logging

logger = logging.getLogger(__name__)


class NotificationSearchView(APIView):

    def get(self, request, *args, **kwargs):
        schema_name = connection.schema_name
        if not schema_name:
            logger.error("No schema name found in the request.")
            return Response(
                {"error": "Schema name not found in the request."}, status=400
            )

        with schema_context(schema_name):
            index_name = get_tenant_index(schema_name)
            logger.debug(f"Using index: {index_name} for tenant: {schema_name}")
            query = {
                "query": {
                    "multi_match": {
                        "query": request.GET.get("q", ""),
                        "fields": ["message"],
                        "fuzziness": "AUTO",
                        "operator": "or",
                    }
                }
            }

            logger.debug(f"Search query: {query}")

            results = search_index(index_name, query)
            logger.debug(f"Elasticsearch returned: {results}")

            if "hits" in results and len(results["hits"]["hits"]) > 0:
                data = [
                    {"id": hit["_id"], **hit["_source"]}
                    for hit in results["hits"]["hits"]
                ]
                logger.debug(f"Serialized data: {data}")
                serializer = NotificationSearchSerializer(data, many=True)
                return Response(serializer.data)
            else:
                logger.debug("No search results found.")
        return Response([], status=200)
