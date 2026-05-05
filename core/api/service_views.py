from rest_framework.views import APIView
from core.services.service_service import ServiceService
from core.utils.response import api_response
from core.auth.permissions import login_required, provider_required
from django.utils.decorators import method_decorator

class ServiceListView(APIView):
    def get(self, request):
        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 20))
        services = ServiceService.get_all_services(page, limit)
        return api_response(True, data=services)

class ServiceCreateView(APIView):
    @method_decorator(provider_required)
    def post(self, request):
        provider_id = request.user_data["user_id"]
        service_id, error = ServiceService.create_service(provider_id, request.data)
        if error:
            return api_response(False, message=error, status_code=400)
        return api_response(True, data={"id": service_id}, message="Service created successfully", status_code=201)

class ServiceDetailView(APIView):
    def get(self, request, service_id):
        service, error = ServiceService.get_service_by_id(service_id)
        if error:
            return api_response(False, message=error, status_code=404)
        return api_response(True, data=service)

    @method_decorator(provider_required)
    def put(self, request, service_id):
        provider_id = request.user_data["user_id"]
        success, error = ServiceService.update_service(service_id, provider_id, request.data)
        if error:
            return api_response(False, message=error, status_code=400)
        return api_response(True, message="Service updated successfully")

    @method_decorator(provider_required)
    def delete(self, request, service_id):
        provider_id = request.user_data["user_id"]
        success, error = ServiceService.delete_service(service_id, provider_id)
        if error:
            return api_response(False, message=error, status_code=400)
        return api_response(True, message="Service deleted successfully")

class ServiceFilterView(APIView):
    def get(self, request):
        category = request.query_params.get("category")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        search = request.query_params.get("search")
        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 20))
        
        services = ServiceService.filter_services(category, min_price, max_price, search, page, limit)
        return api_response(True, data=services)

class ServiceNearbyView(APIView):
    def get(self, request):
        try:
            lat = float(request.query_params.get("lat"))
            lng = float(request.query_params.get("lng"))
            radius = int(request.query_params.get("radius", 5000))
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 20))
        except (TypeError, ValueError):
            return api_response(False, message="Invalid lat, lng, or radius", status_code=400)

        services = ServiceService.search_nearby(lng, lat, radius, page, limit)
        return api_response(True, data=services)
