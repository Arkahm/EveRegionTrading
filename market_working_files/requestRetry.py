def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session



# This return the result of a GET to the given endpoint, with the necessary
#   url added before and after
def get_endpoint(endpoint):

    request_string = \
        ('https://esi.evetech.net/latest'
        '{endpoint}'
        '/?datasource=tranquility&language=en-us').format(endpoint=endpoint)

    c_request = requests_retry_session().get(request_string)
    # c_request = requests.get(request_string)

    # print("Cached: %s" % c_request.from_cache)

    return c_request.json()
