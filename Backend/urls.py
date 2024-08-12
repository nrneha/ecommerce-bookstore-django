from django.urls import path
from Backend import views


urlpatterns = [
    path('View_IndexPage/',views.View_IndexPage,name="View_IndexPage"),
    path('Add_Categories/',views.Add_Categories,name="Add_Categories"),
    path('Save_Categories/',views.Save_Categories,name="Save_Categories"),
    path('View_CategoryData/',views.View_CategoryData,name="View_CategoryData"),
    path('EditPage_Category/<int:c_id>',views.EditPage_Category,name="EditPage_Category"),
    path('Update_CategoryData/<int:c_id>',views.Update_CategoryData,name="Update_CategoryData"),
    path('Delete_CategoryData/<int:c_id>',views.Delete_CategoryData,name="Delete_CategoryData"),
    path('Add_BooksData/',views.Add_BooksData,name="Add_BooksData"),
    path('Save_BookDetails/',views.Save_BookDetails,name="Save_BookDetails"),
    path('View_BookData/',views.View_BookData,name="View_BookData"),
    path('ViewPage_BookEdit/<int:b_id>',views.ViewPage_BookEdit,name="ViewPage_BookEdit"),
    path('Save_updations/<int:b_id>',views.Save_updations,name="Save_updations"),
    path('View_LoginPage/',views.View_LoginPage,name="View_LoginPage"),
    path('Admin_login/',views.Admin_login,name="Admin_login"),
    path('Admin_Logout/',views.Admin_Logout,name="Admin_Logout"),
    path('Customer_Support/',views.Customer_Support,name="Customer_Support"),
    path('CustomerDB_Delete/<int:c_id>',views.CustomerDB_Delete,name="CustomerDB_Delete"),
    path('Delete_Books/<int:b_id>',views.Delete_Books,name="Delete_Books"),
]