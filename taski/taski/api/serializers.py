from rest_framework import serializers


class NotFoundResponseSerializer(serializers.Serializer):
    detail = serializers.JSONField(default={
        "detail": "Not found."
    })


class BadRequestResponseSerializer(serializers.Serializer):
    detail = serializers.JSONField(default={
        "string field": [
            "This field is required."
        ],
        "data field": [
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
        ]
    })
