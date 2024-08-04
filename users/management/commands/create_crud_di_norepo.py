import os
import shutil
from typing import List, Optional

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the app."

    app_name = None
    model_name = None
    parent_target_path = None

    def add_arguments(self, parser):
        parser.add_argument(
            "--create_app",
            action="store_true",
            help="Create the app.",
            default=False,
            required=False,
        )
        parser.add_argument(
            "--app_name", type=str, help="The name of the app.", required=True
        )

        parser.add_argument(
            "--model_name", type=str, help="The name of the model.", required=True
        )

    def handle(self, *args, **options):
        is_new_app = options["create_app"]
        new_app_name = options["app_name"]
        self.parent_target_path = f"./{new_app_name}"
        self.app_name = new_app_name

        model_name = options["model_name"]
        self.model_name = model_name

        if is_new_app:
            print("****** Creating new app ******")
            self.handle_app_creation(new_app_name)
        else:
            print("****** Creating only model in existing app ******")
            self.handle_model_creation(new_app_name, model_name)

    def handle_app_creation(self, app_name):
        exist_app = os.path.exists(self.parent_target_path)

        if exist_app:
            # self.remove_django_app(app_name)
            print(f"App '{app_name}' already exists")
            return
        else:
            self.create_django_app(app_name)

    def handle_model_creation(self, app_name, model_name):
        already_exist_model = os.path.exists(
            f"{self.parent_target_path}/models/{self.calc_filename(model_name)}_model.py"
        )
        if already_exist_model:
            print(f"Model '{model_name}' already exists")
            return

        self.create_model_file(app_name, model_name)
        self.create_other_files(app_name, model_name)
        self.create_service_file(app_name, model_name)
        # self.create_repository_file(app_name, model_name)
        self.update_main_urls_model_creation()
        self.update_di_container(app_name, model_name)

    # ####  Methods ========================
    # ##  Create the app ----------------
    def create_django_app(self, app_name):
        os.system(f"python manage.py startapp {app_name}")
        print(f"Created: {app_name}")

        # ## upd settings.py ------
        self.update_settings(app_name)

        # ## Remove the files that are not needed ------
        paths_to_remove = [
            "views.py",
            "models.py",
            "tests.py",
        ]
        self.remove_several_files(self.parent_target_path, paths_to_remove)

        # ## Create the initial files and folders ------
        self.create_initial_files(app_name, self.model_name)

        # ## Create the model file ------
        self.create_model_file(app_name, self.model_name)

        # ## Create the other files ------
        self.create_other_files(app_name, self.model_name)

        # ## Upd main urls.py ------
        self.update_main_urls()

        # ## Update the DI container ------
        self.update_di_container(app_name, self.model_name)

    def update_settings(self, app_name: str, isCreatingApp: Optional[bool] = True):
        settings_path = "./backend/settings.py"
        with open(settings_path, "r") as file:
            lines = file.readlines()

        # ## Add the app to the INSTALLED_APPS ------
        if isCreatingApp:
            app_line = f"    '{app_name}',\n"
            # search line that contains "# own django apps" and save the index
            start_index = 0
            for i, line in enumerate(lines):
                if "# own django apps" in line:
                    start_index = i
                    break

            # search for the closing bracket from the start_index
            for i, line in enumerate(lines[start_index:], start=start_index):
                if "]" in line:
                    lines.insert(i, app_line)
                    break

            # ## Write the changes
            with open(settings_path, "w") as file:
                file.writelines(lines)
            print(f"Updated: {settings_path}")
        else:
            # ## Remove the app from the INSTALLED_APPS ------
            start_index = 0
            end_index = 0
            for i, line in enumerate(lines):
                if app_name in line:
                    start_index = i
                    break

            for i, line in enumerate(lines[start_index:], start=start_index):
                if "]" in line:
                    end_index = i
                    break

            del lines[start_index:end_index]

            # ## Write the changes
            with open(settings_path, "w") as file:
                file.writelines(lines)
            print(f"Updated: {settings_path}")

    # ##  Remove the app ----------------
    def remove_django_app(self, app_name):
        self.remove_dir(f"./{app_name}")
        # self.delete_all_except_folder(
        #     path=f"./{app_name}",
        #     folder_to_skip="migrations"
        # )

        # ## upd settings.py
        self.update_settings(app_name, isCreatingApp=False)

        # ## upd main urls.py
        self.update_main_urls(isCreatingApp=False)

        # ## recreate the app
        self.create_django_app(app_name)

    # ##  Create initial files ----------------
    def create_initial_files(self, app_name, model_name):
        # ## Create the files and folders
        self.parent_target_path
        paths_to_create = [
            "filters",
            "models",
            "serializers",
            "urls",
            "views",
            "services",
            "repositories",
        ]
        for path in paths_to_create:
            os.makedirs(f"{self.parent_target_path}/{path}", exist_ok=True)
            print(f"Created dir: {path}")

        # ## Create the files
        files_to_create = [
            f"{self.parent_target_path}/filters/__init__.py",
            f"{self.parent_target_path}/models/__init__.py",
            f"{self.parent_target_path}/serializers/__init__.py",
            f"{self.parent_target_path}/urls/__init__.py",
            f"{self.parent_target_path}/views/__init__.py",
            f"{self.parent_target_path}/services/__init__.py",
            f"{self.parent_target_path}/repositories/__init__.py",
        ]
        for file in files_to_create:
            # with open(file, "w") as f:
            #     f.write("# autogenerated file\n")
            print(f"Created file: {file}")

    # ## Create other files ----------------
    def create_other_files(self, app_name, model_name):
        # ## Create the filter file
        self.create_filter_file(app_name, model_name)

        # ## Create the serializer file
        self.create_serializer_file(app_name, model_name)

        # ## Create the views file
        self.create_views_file(app_name, model_name)

        # ## Create the urls file
        self.create_urls_file(app_name, model_name)

        # ## Create the repository file
        # self.create_repository_file(app_name, model_name)

        # ## Create the service file
        self.create_service_file(app_name, model_name)

    # ##  Create the model file ----------------
    def create_model_file(self, app_name, model_name):
        model_file_name = self.calc_filename(model_name) + "_model.py"
        model_file = f"{self.parent_target_path}/models/{model_file_name}"
        with open(model_file, "w") as f:
            f.write(
                f"import uuid\n"
                f"from django.db import models\n\n"
                f"from backend.shared.models.models import AuditDateModel\n\n\n"
                f"class {model_name}(AuditDateModel):\n"
                f"    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)\n"
                f"    pass\n"
            )
        print(f"Created file: {model_file}")

    # ## Create filter file ----------------
    def create_filter_file(self, app_name, model_name):
        filter_file_name = self.calc_filename(model_name) + "_filters.py"
        filter_file = f"{self.parent_target_path}/filters/{filter_file_name}"

        with open(filter_file, "w") as f:
            f.write("from backend.shared.filters.filters import BaseFilter\n")
            f.write(
                f"from {app_name}.models.{self.calc_filename(model_name)}_model import {model_name}\n\n\n"
            )
            f.write(f"class {model_name}Filter(BaseFilter):\n")
            f.write("    class Meta:\n")
            f.write(f"        model = {model_name}\n")
            f.write("        fields = '__all__'\n")

        print(f"Created file: {filter_file}")

    # ## Create serializer file ----------------
    def create_serializer_file(self, app_name, model_name):
        serializer_file_name = self.calc_filename(
            model_name) + "_serializers.py"
        serializer_file = (
            f"{self.parent_target_path}/serializers/{serializer_file_name}"
        )

        with open(serializer_file, "w") as f:
            f.write("from rest_framework import serializers\n\n")
            f.write(
                "from backend.shared.serializers.serializers import (\n"
                "    FiltersBaseSerializer,\n"
                "    QueryDocWrapperSerializer,\n"
                "    QueryListDocWrapperSerializer\n"
                ")\n"
            )
            f.write(
                f"from {app_name}.models.{self.calc_filename(model_name)}_model import {model_name}\n\n\n"
            )

            f.write(f"# ### {model_name} Serializer - Model ===============\n")
            f.write(
                f"class {model_name + 'Serializer'}(serializers.ModelSerializer):\n"
            )
            f.write("    class Meta:\n")
            f.write(f"        model = {model_name}\n")
            f.write("        fields = '__all__'\n\n\n")

            f.write(f"# ## Response: Get All & Get By ID\n")
            f.write(
                f"class {model_name + 'ResponseSerializer'}(FiltersBaseSerializer):\n"
            )
            f.write("    class Meta:\n")
            f.write(f"        model = {model_name}\n")
            f.write("        fields = '__all__'\n\n\n")

            f.write(f"# ### Filter Serializer - Get All ===============\n")
            f.write(
                f"class {model_name + 'FilterSerializer'}(FiltersBaseSerializer):\n"
            )
            f.write("    class Meta:\n")
            f.write(f"        model = {model_name}\n")
            f.write("        fields = '__all__'\n\n\n")

            f.write(f"# ### Swagger ===============\n")
            f.write(f"# ## Response Body: Post & Put & Patch\n")
            f.write(
                f"class {model_name}OptDocWrapperSerializer(QueryDocWrapperSerializer):\n"
            )
            f.write(
                f"    data = {model_name + 'ResponseSerializer'}(required=False)\n\n\n"
            )

            f.write(f"# ## Get All Response\n")
            f.write(
                f"class {model_name}QueryDocWrapperSerializer(QueryListDocWrapperSerializer):\n"
            )
            f.write(
                f"    data = {model_name + 'ResponseSerializer'}(many=True, required=False)\n"
            )

        print(f"Created file: {serializer_file}")

    # ## Create the views file ----------------
    def create_views_file(self, app_name, model_name):
        views_file_name = self.calc_filename(model_name) + "_views.py"
        views_file = f"{self.parent_target_path}/views/{views_file_name}"

        with open(views_file, "w") as f:
            f.write("# ## docs openapi\n")
            f.write("from drf_yasg.utils import swagger_auto_schema\n")
            f.write("from drf_yasg import openapi\n\n\n")

            f.write("from backend.shared.di.di import container\n")
            f.write(
                "from backend.shared.views.base_view import (\n"
                "    GenericAPIViewService,\n"
                "    BaseUpdateView,\n"
                "    BaseRetrieveUuidView,\n"
                ")\n"
            )
            f.write(
                "from backend.shared.serializers.serializers import (\n"
                "    BadRequestSerializer,\n"
                "    NotFoundSerializer,\n"
                ")\n\n"
            )
            f.write(
                "from backend.shared.constants.common_constants import page_size_openapi, page_openapi\n"
            )

            # ## solo quedaria para type el service
            # f.write(
            #     f"from {app_name}.repositories.{self.calc_filename(model_name)}_repository import {model_name}Repository\n"
            # )
            # f.write(
            #     f"from {app_name}.services.{self.calc_filename(model_name)}_service import {model_name}Service\n"
            # )
            f.write(
                f"from {app_name}.serializers.{self.calc_filename(model_name)}_serializers import (\n"
                f"    {model_name + 'Serializer'},\n"
                f"    {model_name + 'QueryDocWrapperSerializer'},\n"
                f"    {model_name + 'OptDocWrapperSerializer'},\n"
                f"    {model_name + 'FilterSerializer'},\n"
                ")\n\n\n"
            )

            # ## View 1 -----------------
            f.write(f"class {model_name + 'View'}(GenericAPIViewService):\n\n")
            f.write(f"    # constructor: DI\n")
            f.write(f"    def __init__(self):\n")
            f.write(
                f"        {self.calc_filename(model_name)}_service = container.{self.calc_filename(model_name)}_service()\n"
            )
            f.write(
                f"        super().__init__({self.calc_filename(model_name)}_service)\n\n"
            )

            f.write(
                f"    @swagger_auto_schema(\n"
                f'        operation_description="Get All {model_name}s",\n'
                f"        responses={{\n"
                f'            200: openapi.Response("OK", {model_name + "QueryDocWrapperSerializer"}),\n'
                f"        }},\n"
                f'        query_serializer={model_name + "FilterSerializer"},\n'
                f"        manual_parameters=[page_size_openapi, page_openapi],\n"
                f"    )\n"
            )
            f.write(f"    def get(self, request):\n")
            f.write(f"        return super().get(request)\n\n")

            f.write(
                f"    @swagger_auto_schema(\n"
                f'        operation_description="Create {model_name}",\n'
                f'        request_body={model_name + "Serializer"},\n'
                f"        responses={{\n"
                f'            201: openapi.Response("OK", {model_name + "OptDocWrapperSerializer"}),\n'
                f'            400: openapi.Response("Bad Request", BadRequestSerializer),\n'
                f"        }},\n"
                f"    )\n"
            )
            f.write(f"    def post(self, request):\n")
            f.write(f"        return super().post(request)\n\n\n")

            # ## View 2 -----------------
            f.write(
                f"class {model_name + 'DetailView'}(BaseUpdateView):\n\n"
            )
            f.write(f"    # constructor: DI\n")
            f.write(f"    def __init__(self):\n")
            f.write(
                f"        {self.calc_filename(model_name)}_service = container.{self.calc_filename(model_name)}_service()\n"
            )
            f.write(
                f"        super().__init__({self.calc_filename(model_name)}_service)\n\n"
            )

            # f.write(
            #     f"    @swagger_auto_schema(\n"
            #     f'        operation_description="Get {model_name} by ID",\n'
            #     f"        responses={{\n"
            #     f'            200: openapi.Response("OK", {model_name + "OptDocWrapperSerializer"}),\n'
            #     f'            404: openapi.Response("Not Found", NotFoundSerializer),\n'
            #     f"        }},\n"
            #     f"    )\n"
            # )
            # f.write(f"    def get(self, request, pk):\n")
            # f.write(f"        return super().get(request, pk)\n\n")

            f.write(
                f"    @swagger_auto_schema(\n"
                f'        operation_description="Update {model_name}",\n'
                f"        request_body={model_name + 'Serializer'},\n"
                f"        responses={{\n"
                f'            200: openapi.Response("OK", {model_name + "OptDocWrapperSerializer"}),\n'
                f'            404: openapi.Response("Not Found", NotFoundSerializer),\n'
                f'            400: openapi.Response("Bad Request", BadRequestSerializer),\n'
                f"        }},\n"
                f"    )\n"
            )
            f.write(f"    def patch(self, request, pk):\n")
            f.write(f"        return super().patch(request, pk)\n\n")

            # f.write(
            #     f"    @swagger_auto_schema(\n"
            #     f'        operation_description="Delete {model_name}",\n'
            #     f"        responses={{\n"
            #     f'            204: openapi.Response("Ok - No Content"),\n'
            #     f'            404: openapi.Response("Not Found", NotFoundSerializer),\n'
            #     f"            401: openapi.Response('Unauthorized'),\n"
            #     f"        }},\n"
            #     f"    )\n"
            # )
            # f.write(f"    def delete(self, request, pk):\n")
            # f.write(f"        return super().delete(request, pk)\n\n\n")

            # ---- Get By UUID:
            f.write(
                f"class {model_name + 'DetailViewByUuid'}(BaseRetrieveUuidView):\n")
            f.write(f"    # constructor: DI\n")
            f.write(f"    def __init__(self):\n")
            f.write(
                f"        {self.calc_filename(model_name)}_service = container.{self.calc_filename(model_name)}_service()\n"
            )
            f.write(
                f"        super().__init__({self.calc_filename(model_name)}_service)\n\n"
            )
            f.write(
                f"    @swagger_auto_schema(\n"
                f'        operation_description="Get {model_name} by UUID",\n'
                f"        responses={{\n"
                f'            200: openapi.Response("OK", {model_name + "OptDocWrapperSerializer"}),\n'
                f'            404: openapi.Response("Not Found", NotFoundSerializer),\n'
                f"        }},\n"
                f"    )\n"
            )
            f.write(f"    def get(self, request, uuid):\n")
            f.write(f"        return super().get(request, uuid)\n")

        print(f"Created file: {views_file}")

    # ## Create the urls file ----------------
    def create_urls_file(self, app_name, model_name):
        urls_file_name = self.calc_filename(model_name) + "_urls.py"
        urls_file = f"{self.parent_target_path}/urls/{urls_file_name}"

        with open(urls_file, "w") as f:
            f.write("from django.urls import path\n\n")
            f.write(
                f"from {app_name}.views.{self.calc_filename(model_name)}_views import (\n"
                f"    {model_name}View,\n"
                f"    {model_name}DetailView,\n"
                f"    {model_name}DetailViewByUuid,\n"
                ")\n\n\n"
            )
            f.write(
                f"urlpatterns = [\n"
                f"    path('', {model_name}View.as_view(), name='{self.calc_filename(model_name)}'),\n"
                f"    path('<int:pk>/', {model_name}DetailView.as_view(), name='{self.calc_filename(model_name)}-detail'),\n"
                f"    path('<str:uuid>/', {model_name}DetailViewByUuid.as_view(), name='{self.calc_filename(model_name)}-detail-uuid'),\n"
                f"]\n"
            )

        print(f"Created file: {urls_file}")

    # ## Upd main urls.py ----------------
    def update_main_urls(self, isCreatingApp: Optional[bool] = True):
        main_urls_path = "./backend/urls.py"
        comment_to_find = "# ### API"

        urls_line = f'    path("api/v1/{self.calc_filename(self.model_name)}/", include("{self.calc_filename(self.app_name)}.urls.{self.calc_filename(self.model_name)}_urls")),\n\n'

        with open(main_urls_path, "r") as file:
            lines = file.readlines()

        if isCreatingApp:
            # ## Add the app to the main urls.py ------
            # search line that contains "# ### API" and save the index
            start_index = 0
            for i, line in enumerate(lines):
                if comment_to_find in line:
                    start_index = i
                    break

            # search for the closing bracket from the start_index
            for i, line in enumerate(lines[start_index:], start=start_index):
                if "]" in line:
                    lines.insert(i, urls_line)
                    break

            # ## Write the changes
            with open(main_urls_path, "w") as file:
                file.writelines(lines)
        else:  # ya no se usa
            # line to remove
            line_to_remove = urls_line

            # ## Remove the app from the main urls.py ------
            start_index = 0
            end_index = 0
            for i, line in enumerate(lines):
                if line_to_remove in line:
                    start_index = i
                    break

            for i, line in enumerate(lines[start_index:], start=start_index):
                if "]" in line:
                    end_index = i
                    break

            del lines[start_index:end_index]

            # ## Write the changes
            with open(main_urls_path, "w") as file:
                file.writelines(lines)

        print(f"Updated: {main_urls_path}")

    def update_main_urls_model_creation(self):
        main_urls_path = "./backend/urls.py"
        comment_to_find = "# ### API"

        urls_line = f'    path("api/v1/{self.calc_filename(self.model_name)}/", include("{self.calc_filename(self.app_name)}.urls.{self.calc_filename(self.model_name)}_urls")),\n\n'

        with open(main_urls_path, "r") as file:
            lines = file.readlines()

        # ## Add the app to the main urls.py ------
        # search line that contains "# ### API" and save the index
        start_index = 0
        for i, line in enumerate(lines):
            if comment_to_find in line:
                start_index = i
                break

        # search for the closing bracket from the start_index
        for i, line in enumerate(lines[start_index:], start=start_index):
            if "]" in line:
                lines.insert(i, urls_line)
                break

        # ## Write the changes
        with open(main_urls_path, "w") as file:
            file.writelines(lines)

        print(f"Updated: {main_urls_path}")

    # ## Create repository file ----------------
    def create_repository_file(self, app_name, model_name):
        repository_file_name = self.calc_filename(
            model_name) + "_repository.py"
        repository_file = (
            f"{self.parent_target_path}/repositories/{repository_file_name}"
        )

        with open(repository_file, "w") as f:
            f.write("from typing import Type\n\n")
            f.write(
                "from backend.shared.repositories.base_repository import BaseRepository\n\n"
            )
            f.write(
                f"from {app_name}.models.{self.calc_filename(model_name)}_model import {model_name}\n\n\n"
            )
            f.write(f"class {model_name + 'Repository'}(BaseRepository):\n")
            f.write(f"    model: Type[{model_name}]\n\n")
            f.write(f"    def __init__(self, model):\n")
            f.write(f"        super().__init__(model)\n")

    # ## Create service file ----------------
    def create_service_file(self, app_name, model_name):
        service_file_name = self.calc_filename(model_name) + "_service.py"
        service_file = f"{self.parent_target_path}/services/{service_file_name}"

        with open(service_file, "w") as f:
            f.write("from typing import Type\n\n")
            f.write(
                "from backend.shared.services.base_service import BaseService\n\n")
            # f.write(
            #     f"from {app_name}.repositories.{self.calc_filename(model_name)}_repository import {model_name}Repository\n"
            # )
            f.write(
                f"from {app_name}.models.{self.calc_filename(model_name)}_model import {model_name}\n"
            )
            f.write(
                f"from {app_name}.filters.{self.calc_filename(model_name)}_filters import {model_name}Filter\n"
            )
            f.write(
                f"from {app_name}.serializers.{self.calc_filename(model_name)}_serializers import (\n"
                f"    {model_name + 'Serializer'},\n"
                f"    {model_name + 'ResponseSerializer'},\n"
                ")\n\n\n"
            )
            f.write(f"class {model_name + 'Service'}(BaseService):\n")
            # f.write(f"    repository: Type[{model_name}Repository]\n\n")
            f.write(f"    model: Type[{model_name}]\n\n")
            f.write(f"    filter = Type[{model_name}Filter]\n\n")
            f.write(f"    serializer = Type[{model_name + 'Serializer'}]\n")
            f.write(
                f"    serializer2 = Type[{model_name + 'ResponseSerializer]'}\n\n")
            f.write(f"    def __init__(self, model):\n")
            f.write(f"        filter = {model_name}Filter\n")
            f.write(f"        serializer = {model_name + 'Serializer'}\n")
            f.write(
                f"        serializer2 = {model_name + 'ResponseSerializer'}\n")
            f.write(
                f"        super().__init__(model, filter, serializer, serializer2)\n")

    def update_di_container(self, app_name, model_name):
        container_file_name = f"./backend/shared/di/di.py"
        # if not exist, create the file and create __init__.py in the folder
        if not os.path.exists(container_file_name):
            with open(container_file_name, "w") as f:
                f.write(
                    "from dependency_injector import containers, providers\n\n\n")
                f.write("class Container(containers.DeclarativeContainer):\n\n\n")
                f.write("container = Container()\n")
            print(f"Created file: {container_file_name}")

            # create __init__.py
            open(f"./../backend/shared/di/__init__.py", "w").close()
            print("Created file: __init__.py")

        # ## Add imports ------
        # find the last line of the file that includes `from ... import ...` and add the new imports
        last_import_search = "end imports ---"
        last_line_index = 0
        with open(container_file_name, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if last_import_search in line:
                    last_line_index = i

        # add the new imports
        new_imports = [
            f"from {app_name}.models.{self.calc_filename(model_name)}_model import {model_name}\n",
            f"from {app_name}.services.{self.calc_filename(model_name)}_service import {model_name}Service\n\n",
        ]
        lines.insert(last_line_index + 2, new_imports[0])
        lines.insert(last_line_index + 3, new_imports[1])

        # ## Write the changes
        with open(container_file_name, "w") as file:
            file.writelines(lines)

        print(f"Updated: {container_file_name}")

        # ## Add the service to the DI container ------
        # find the last line of the file that includes `# end di ---` and save the index
        last_param_search = "# end di ---"
        last_line_index = 0
        container_declaration = "container = Container()"
        container_declaration_index = 0

        with open(container_file_name, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if last_param_search in line:
                    last_line_index = i
                if container_declaration in line:
                    container_declaration_index = i

        # add the new model to the container
        new_model = f"    {self.calc_filename(model_name)}_model = providers.Object({model_name})\n"
        # add the new service to the container
        new_service = f"    {self.calc_filename(model_name)}_service = providers.Singleton({model_name}Service, model={self.calc_filename(model_name)}_model)\n"

        # Insert the new lines before `# end di ---`
        lines.insert(last_line_index, new_model)
        lines.insert(last_line_index + 1, new_service)
        lines.insert(last_line_index + 2, "\n")

        # Ensure `container = Container()` remains at the end
        container_line = lines.pop(container_declaration_index)
        lines.append(container_line)

        # ## Write the changes
        with open(container_file_name, "w") as file:
            file.writelines(lines)

        print(f"Updated: {container_file_name}")

    # ####  Aux Functions ========================
    def remove_dir(self, path):
        try:
            shutil.rmtree(path)
            print(f"Removed dir: {path}")
        except OSError as e:
            print(f"Error: {e.strerror}")

    def remove_several_files(self, path, files: List[str]):
        for file in files:
            try:
                os.remove(f"{path}/{file}")
                print(f"Removed file: {file}")
            except OSError as e:
                print(f"Error: {e.strerror}")

    def calc_filename(self, name: str) -> str:
        name = name.replace(" ", "_")
        name = name[0].lower() + name[1:]
        i = 0
        while i < len(name):
            if name[i].isupper():
                name = name[:i] + "_" + name[i].lower() + name[i + 1:]
                i += 1  # Skip the underscore on the next iteration
            i += 1
        return name

    def delete_all_except_folder(self, path, folder_to_skip):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if filename == folder_to_skip and os.path.isdir(file_path):
                continue
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
