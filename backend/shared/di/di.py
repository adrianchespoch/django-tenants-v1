from dependency_injector import containers, providers

from users.models.user_model import User
from users.services.user_serice import UserService

from users.models.extended_group_model import ExtendedGroup
from users.services.extended_group_service import ExtendedGroupService

from users.services.auth_service import AuthService
from django.contrib.auth.models import Group, Permission
# end imports ---


class Container(containers.DeclarativeContainer):
    # Manager isn't accessible via Publisher instances - Error cuando se inyecta la instancia y no el modelo (sol. Object)
    user_model = providers.Object(User)
    user_service = providers.Singleton(
        UserService, model=user_model
    )
    extended_group_model = providers.Object(ExtendedGroup)
    extended_group_service = providers.Singleton(
        ExtendedGroupService, model=extended_group_model)

    auth_service = providers.Singleton(
        AuthService, group_model=providers.Object(Group), permission_model=providers.Object(Permission), user_model=user_model, 
        extended_group_model=extended_group_model)

    # end di ---

container = Container()
