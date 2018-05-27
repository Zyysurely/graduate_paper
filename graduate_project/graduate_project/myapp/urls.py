from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'init_network$', views.get_network, ),
    url(r'fresh_network$', views.fresh_network, ),
    url(r'run_al$', views.run_al, ),
    url(r'login$', views.login, ),
    url(r'get_task_list$', views.get_task_list, ),
    url(r'get_task_network$', views.get_task_network, ),
    url(r'get_demo_network$', views.get_demo_by_task, ),
    url(r'del_task$', views.del_task, ),
    url(r'get_dataset_list$', views.get_dataset_list, ),
    url(r'operate_dataset$', views.operate_dataset, ),
    url(r'upload_dataset$', views.upload_dataset, ),
    url(r'get_user_list$', views.get_user_list, ),
]