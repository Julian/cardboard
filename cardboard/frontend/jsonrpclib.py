import json


class JSONRPCError(Exception):
    def __init__(self, data=None, *args, **kwargs):
        super(JSONRPCError, self).__init__(*args, **kwargs)
        self.data = data

    def __str__(self):
        return self.message

    def to_response(self):
        return {
            "code" : self.code, "message" : self.message, "data" : self.data
        }


class ParseError(JSONRPCError):
    code = -32700
    message = "Parse error"


class InvalidRequest(JSONRPCError):
    code = -32600
    message = "Invalid request"


class MethodNotFound(JSONRPCError):
    code = -32601
    message = "Message not found"


class InvalidParams(JSONRPCError):
    code = -32602
    message = "Invalid params"


class InternalError(JSONRPCError):
    code = -32603
    message = "Internal error"


class ApplicationError(JSONRPCError):
    def __init__(self, code, message, data=None, *args, **kwargs):
        super(ApplicationError, self).__init__(data=data, *args, **kwargs)

        self.code = code
        self.message = message


class ServerError(JSONRPCError):
    message = "Server error"

    def __init__(self, code, data=None, *args, **kwargs):
        if not -32099 <= code <= -32000:
            raise ValueError("Invalid server error code")

        super(ServerError, self).__init__(data=data, *args, **kwargs)
        self.code = code


class InvalidResponse(JSONRPCError):
    pass


_e = {ParseError, InvalidRequest, MethodNotFound, InvalidParams, InternalError}
PROTOCOL_ERRORS = {error.code : error for error in _e}


def error(id, failure):
    tr = getattr(failure.value, "to_response", None)
    if tr is None:
        tr = InternalError({
            "message" : failure.getErrorMessage(),
            "exception" : failure.type.__name__,
            "traceback" : failure.getTraceback(),
        }).to_response
    return json.dumps({"jsonrpc" : "2.0", "id" : id, "error" : tr()})


def notify(method, params=()):
    notification = {"jsonrpc" : "2.0", "method" : method, "params" : params}
    return json.dumps(notification)


def request(id, method, params=()):
    req = {"jsonrpc" : "2.0", "id" : id, "method" : method, "params" : params}
    return json.dumps(req)


def response(id, result):
    return json.dumps({"jsonrpc" : "2.0", "id" : id, "result" : result})


def loads(data):
    try:
        return json.loads(data)
    except ValueError:
        raise ParseError()


def received_result(recv):
    if "jsonrpc" not in recv:
        raise InvalidRequest({"reason" : "jsonrpc"})
    elif "id" not in recv:
        raise InvalidRequest({"reason" : "id"})
    elif "result" in recv and "error" in recv:
        raise InvalidRequest(
            {"reason" : "Cannot contain both 'result' and 'error'"}
        )
    elif "result" in recv:
        result = recv["result"]
    elif "error" in recv:
        err = recv["error"]

        try:
            code, message = int(err["code"]), err["message"]
        except (KeyError, TypeError, ValueError) as e:
            raise InvalidResponse(e.args[0])
        data = err.get("data")

        if code in PROTOCOL_ERRORS:
            raise PROTOCOL_ERRORS[code](data=data)
        else:
            try:
                err = ServerError(code=code, data=data)
            except ValueError:
                err = ApplicationError(code=code, message=message, data=data)
            raise err
    else:
        raise InvalidRequest({"reason" : "error"})
    return recv


def received_request(recv, methods):
    if "jsonrpc" not in recv:
        raise InvalidRequest({"reason" : "jsonrpc"})
    elif "method" not in recv:
        raise InvalidRequest({"reason" : "method"})

    method = recv["method"]
    params = recv.get("params", [])

    if method not in methods:
        raise MethodNotFound({"method" : method})

    try:
        params.keys
    except AttributeError:
        try:
            iter(params)
        except TypeError:
            raise InvalidParams(
                {"reason" : "{!r} is not dict or list-like".format(params)}
            )
        else:
            recv["args"], recv["kwargs"] = params, {}
    else:
        recv["args"], recv["kwargs"] = [], params
    return recv
