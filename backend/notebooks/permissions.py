from rest_framework.permissions import BasePermission


class IsNotebookOwner(BasePermission):
    """
    Allows access only to the owner of the notebook.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user