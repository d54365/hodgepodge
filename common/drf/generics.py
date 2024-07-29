from rest_framework.generics import GenericAPIView as GenericAPIView_


class GenericAPIView(GenericAPIView_):
    service = None

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        action = self.action  # noqa
        serializer_cls = None
        if action == "list":
            if hasattr(self, "list_serializer_class"):
                serializer_cls = getattr(self, "list_serializer_class")
        elif action == "retrieve":
            if hasattr(self, "retrieve_serializer_class"):
                serializer_cls = getattr(self, "retrieve_serializer_class")
        elif action == "create":
            if hasattr(self, "create_serializer_class"):
                serializer_cls = getattr(self, "create_serializer_class")
        elif action == "update":
            if hasattr(self, "update_serializer_class"):
                serializer_cls = getattr(self, "update_serializer_class")
        if serializer_cls is None:
            serializer_cls = self.serializer_class

        return serializer_cls
