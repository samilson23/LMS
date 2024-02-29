from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class ActiveUserCount(MiddlewareMixin):
    def process_request(self, request):
        active_users = cache.get('active_users', 0)
        active_users += 1
        cache.set('active_users', active_users)

    def process_response(self, request, response):
        active_users = cache.get('active_users', 0)
        active_users -= 1
        cache.set('active_users', active_users)
        return response
