from backend.shared.mixins.common_mixin import AuthenticationViewMixin, PermissionRequiredViewMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, RetrieveViewMixin, DestroyViewMixin, RetrievePkViewMixin


class GenericAPIViewService(AuthenticationViewMixin, PermissionRequiredViewMixin, ListViewMixin, CreateViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class GenericAPIDetailViewService(AuthenticationViewMixin, PermissionRequiredViewMixin, RetrieveViewMixin, UpdateViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class GenericAPIDetailAllViewService(AuthenticationViewMixin, PermissionRequiredViewMixin, CreateViewMixin, RetrieveViewMixin, UpdateViewMixin, DestroyViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


# UUID
class BaseGetAllView(AuthenticationViewMixin, PermissionRequiredViewMixin, ListViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class BaseRetrieveUuidView(AuthenticationViewMixin, PermissionRequiredViewMixin, RetrieveViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class BaseRetrievePkView(AuthenticationViewMixin, PermissionRequiredViewMixin, RetrievePkViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class BaseUpdateView(AuthenticationViewMixin, PermissionRequiredViewMixin, UpdateViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class BaseDestroyView(AuthenticationViewMixin, PermissionRequiredViewMixin, DestroyViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


# ### Free views ------------------------------
class BaseGetAllFreeView(ListViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class BaseCreateFreeView(CreateViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class BaseRetrieveFreeView(RetrieveViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()


class BaseUpdateFreeView(UpdateViewMixin):
    # DI: service
    def __init__(self, service):
        self.service = service
        super().__init__()
