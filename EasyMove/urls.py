from django.urls import path
from . import views
app_name = 'EasyMove'
urlpatterns = [
    #item list view
    path('', views.home, name='easy-move-home'),
    path('item-list', views.easy_move_list, name = 'easy-move-list'),
    path('items/<int:item_id>', views.easy_move_items_detail, name="item-detail"),
    path('items/add-item', views.easy_move_add_item, name="add-item"),
    path('items/edit-item/<int:item_id>', views.easy_move_edit_item, name="edit-item"),
    path('items/edit-item/submit-edit/<int:item_id>',views.easy_move_submit_edit,name="submit-edit"),
    path('items/delete-item/<int:item_id>', views.easy_move_delete_item, name="delete-item"),
    path('change-location', views.easy_move_change_location, name="change-location"),
    path('items/<int:item_id>/compare', views.easy_move_item_compare, name="compare-item"),
    path('items/add-comment', views.new_comment_add,name="add-comment"),
    path('delete-comment', views.delete_comment, name="delete-comment"),
    path('edit-comment', views.edit_comment, name="edit-comment"),
    path('items/change-role', views.update_user_role, name="change-role"),
]