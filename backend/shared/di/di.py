from dependency_injector import containers, providers

from users.models.user_model import User
from users.services.user_serice import UserService

from users.models.extended_group_model import ExtendedGroup
from users.services.extended_group_service import ExtendedGroupService

from users.services.auth_service import AuthService
from django.contrib.auth.models import Group, Permission

from multicpy.models.suscripcion_model import Suscripcion
from multicpy.services.suscripcion_service import SuscripcionService
from multicpy.models.empresa_model import Empresa
from multicpy.services.empresa_service import EmpresaService
# end imports ---

from books.models.book_model import Book
from books.services.book_service import BookService


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

    empresa_model = providers.Object(Empresa)
    empresa_service = providers.Singleton(EmpresaService, model=empresa_model)
    suscripcion_model = providers.Object(Suscripcion)
    suscripcion_service = providers.Singleton(SuscripcionService, model=suscripcion_model)
    book_model = providers.Object(Book)
    book_service = providers.Singleton(BookService, model=book_model)
    # end di ---

container = Container()


