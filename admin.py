from sqladmin import Admin, ModelView
from wtforms.fields.simple import TextAreaField

from database import engine
from main import app
from models import Basket

admin = Admin(app=app, engine=engine)

class BasketAdmin(ModelView, model = Basket):
    name = 'Basket'
    icon = "fa-solid fa-basket-shopping"

    column_list = [Basket.id, Basket.id_doc, Basket.doc_date]
    column_searchable_list = [Basket.id, Basket.doc_date]
    column_sortable_list = [Basket.id, Basket.doc_date]

    form_overrides = {
        "goods_json": TextAreaField
    }

admin.add_view(BasketAdmin)