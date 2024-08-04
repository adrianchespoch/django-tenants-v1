from backend.shared.filters.filters import BaseFilter
from users.models.user_model import User


class UserFilter(BaseFilter):
    class Meta:
        model = User
        fields = '__all__'
