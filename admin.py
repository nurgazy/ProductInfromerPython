from sqladmin import Admin, ModelView
from wtforms.fields.simple import TextAreaField, PasswordField

from database import engine
from models import Basket, User


class BasketAdmin(ModelView, model = Basket):
    name = 'Корзина'
    name_plural = 'Корзина'
    icon = "fa-solid fa-basket-shopping"

    column_list = [Basket.id, Basket.id_doc, Basket.doc_date]
    column_searchable_list = [Basket.id, Basket.doc_date]
    column_sortable_list = [Basket.id, Basket.doc_date]

    form_overrides = {
        "goods_json": TextAreaField
    }


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-users"

    column_list = [User.id, User.username, User.role]
    form_columns = ["username", "password_hash", "role", "api_token"]

    form_overrides = {"password_hash": PasswordField}
    form_args = {
        "password_hash": {"label": "Пароль"},
        "api_token": {"label": "API Токен (для мобильных, оставьте пустым для автогенерации)"}
    }

def init_admin(app_instance):
    admin_instance = Admin(app=app_instance, engine=engine)
    admin_instance.add_view(BasketAdmin)
    admin_instance.add_view(UserAdmin)
    return admin_instance