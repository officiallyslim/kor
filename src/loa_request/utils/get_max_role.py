from src.loa_request.data.roles_hierarchy import (
    builder_roles_hierarchy,
    moderator_roles_hierarchy,
)

def get_max_builder(auhor_roles):
    levels = [
        builder_roles_hierarchy.get(role.id, {}).get("level", 0) for role in auhor_roles
    ]

    max_level = max(levels, default=None)

    if max_level is not None:
        max_role = next(
            (
                role
                for role in auhor_roles
                if builder_roles_hierarchy.get(role.id, {}).get("level") == max_level
            ),
            None,
        )
        if max_role:
            return max_role
        else:
            return "No builder role"
    else:
        return "No builder role"


def get_max_moderator(auhor_roles):
    levels = [
        moderator_roles_hierarchy.get(role.id, {}).get("level", 0)
        for role in auhor_roles
    ]

    max_level = max(levels, default=None)

    if max_level is not None:
        max_role = next(
            (
                role
                for role in auhor_roles
                if moderator_roles_hierarchy.get(role.id, {}).get("level") == max_level
            ),
            None,
        )
        if max_role:
            return max_role
        else:
            return "No moderator role"
    else:
        return "No moderator role"