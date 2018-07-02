from django.conf.urls import include, url
from . import views
from amazi_meza_app.backend import handel_rapidpro_request
#from djgeojson.views import TiledGeoJSONLayerView
#from amazi_meza_app.models import WaterSourceEndPoint

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^home$', views.home, name='home'),
    url(r'^problems$', views.problems, name='problems'),
    url(r'^mapping$', views.mapping, name='mapping'),
    url(r'^finance$', views.finance, name='finance'),
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
    url(r'^getcollinesincommune', views.getCollinesInCommune, name='getcollinesincommune'),
    url(r'^getcommunesinprovince', views.getCommunesInProvince, name='getcommunesinprovince'),
    url(r'^getwanteddata', views.getwanteddata, name='getwanteddata'),
    url(r'^getnumberofwaterpoints', views.get_number_of_water_points, name='getnumberofwaterpoints'),
    url(r'^getexpenditures', views.get_expenditures_info, name='getexpenditures'),
    url(r'^get_exp_vs_in', views.exp_vs_in, name='get_exp_vs_in'),
]