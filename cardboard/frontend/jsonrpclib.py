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


class ServerError(JSONRPCError):
    message = "Server error"

    def __init__(self, code, data=None, *args, **kwargs):
        if not -32099 <= code <= -32000:
            raise ValueError("Invalid server error code")

        super(ServerError, self).__init__(data=data, *args, **kwargs)
        self.code = code


_ERRORS = {ParseError, InvalidRequest, MethodNotFound, InternalError}
PROTOCOL_ERRORS = {error.code : error for error in _ERRORS}


def error(id, err):
    err = {"jsonrpc" : "2.0", "id" : id, "error" : err.to_response()}
    return json.dumps(err)


def notify(method, params=()):
    notification = {"jsonrpc" : "2.0", "method" : method, "params" : params}
    return json.dumps(notification)


def request(id, method, params=()):
    req = {"jsonrpc" : "2.0", "id" : id, "method" : method, "params" : params}
    return json.dumps(req)


def response(id, result):
    return json.dumps({"jsonrpc" : "2.0", "id" : id, "result" : result})


def received(data):
    try:
        recv = json.loads(data)
    except ValueError:
        raise ParseError()

    if "jsonrpc" not in recv:
        raise InvalidRequest("jsonrpc")

    if "result" in recv or "error" in recv:
        return _received_result(recv)
    else:
        return _received_request(recv)


def _received_result(recv):
    if "id" not in recv:
        raise InvalidRequest("id")

    if "result" in recv and "error" in recv:
        raise InvalidRequest("Cannot contain both 'result' and 'error'")
    elif "result" in recv:
        result = recv["result"]
    elif "error" in recv:
        err = recv["error"]
    return recv


def _received_request(recv):
    if "method" not in recv:
        raise InvalidRequest("method")
    params = recv.get("params", [])

    try:
        params.keys
    except AttributeError:
        try:
            iter(params)
        except TypeError:
            raise InvalidParams(params)
        else:
            recv["args"], recv["kwargs"] = params, {}
    else:
        recv["args"], recv["kwargs"] = [], params
    return recv
