from rest_framework import permissions


class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'HEAD': [],
        'OPTIONS': [],
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    # def has_permission(self, request, view):
    #     if not request.user.is_staff:
    #         return False
    #     return super().has_permission(request, view)

    # def has_permission(self, request, view):
    #     user = request.user
    #     print(user.get_all_permissions())
    #     return user.is_staff and (
    #         user.has_perm("products.add_product") or
    #         user.has_perm("products.view_product") or
    #         user.has_perm("products.change_product") or
    #         user.has_perm("products.delete_product")
    #     )
