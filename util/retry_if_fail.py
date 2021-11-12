import traceback


def retry_if_fail(retry_times=3):
    """
    It only checks the root level error to check if NASDA works well.
    :param retry_times:
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kw):
            r = retry_times
            exception = None
            while r:
                try:
                    response = func(*args, **kw)
                    doc = xml.dom.minidom.parseString(response)
                    error_nodes = doc.getElementsByTagNameNS('', 'errorCode')
                    if not error_nodes:
                        log.debug(response)
                        raise Exception("Error happened when accessing XXX")
                    error_code = error_nodes[0].firstChild.nodeValue
                    if error_code != '':
                        log.debug(response)
                        raise Exception("Error happened when accessing XXX : %s "
                                        .format(error_code.decode('utf-8') if sys.version_info.major == 2 else error_code))
                    return error_nodes[0].nextSibling
                except Exception as e:
                    r -= 1
                    exception = e
                    log.debug(traceback.format_exc())
            if exception:
                raise exception

        return wrapper

    return decorator