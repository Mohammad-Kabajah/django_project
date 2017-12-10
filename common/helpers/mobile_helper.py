__author__ = 'Abdulhafeth'

def is_mobile_app(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if user_agent:
        user_agent = user_agent.lower()

    if 'dalvik' in user_agent or 'cfnetwork' in user_agent or "alamofire" in user_agent:
        return True

    return False