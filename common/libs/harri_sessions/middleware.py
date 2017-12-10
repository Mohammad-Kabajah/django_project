__author__ = 'omar'

from django.conf import settings

class CrossDomainSessionMiddleware(object):
    """
    This small hack sets all the cookies' domain to the actual domain that was requested originally
    This is only useful when you have multiple domains pointing to the same server, for example harri.com and
    teamwork.com
    """
    def process_response(self, request, response):
        if response.cookies:
            host = request.get_host()
            print "hoost>>>>>>>",host
            #this converts api.harri.com to .harri.com
            domain = self._build_domain_name(host)

            print "domainnn>>>>", domain
            # check if it's a different domain
            if settings.SESSION_COOKIE_DOMAIN and domain != settings.SESSION_COOKIE_DOMAIN:
                for cookie in response.cookies:
                    if 'domain' in response.cookies[cookie]:
                        response.cookies[cookie]['domain'] = domain
        return response

    def _build_domain_name(self, host):
        try:
            #split api.harri.com to [api,harri,com]
            domain_parts = host.split('.')
            #now just t ake the last two parts to produce the following => .harri.com
            domain = ".{second_last_part}.{last_part}".\
                format(second_last_part=domain_parts[-2], last_part=domain_parts[-1])

            return domain

        except Exception:
            return None


