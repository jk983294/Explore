from .._pyprotos import contest_pb2 as pb2, contest_pb2_grpc as pb2_grpc
from .GlobalInfo import GlobalInfo
import grpc
from concurrent import futures
from collections import deque
import time


class AnswerService(pb2_grpc.ContestServicer):
    def __init__(self, port, global_info: GlobalInfo):
        self.answers = deque(maxlen=2000)
        self.account_manager = global_info.accountManager
        self.mode = global_info.mode
        self.current_answer = None
        self.current_question = None
        self.logger = global_info.logger

        # gRPC server
        self._server = None
        self._port = port

    def start(self):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_ContestServicer_to_server(self, self._server)

        self._server.add_insecure_port('[::]:%d' % self._port)
        self._server.start()

    def stop(self):
        if self._server:
            self._server.stop(0).wait()
            del self._server
            self._server = None

    # API:

    def login(self, request: pb2.LoginRequest, context):
        account = self.account_manager.get_account(request.user_id)

        response = pb2.UserLoginResponse()
        if account and account.pin == request.user_pin:
            response.success = True
            response.user_id = account.id
            response.user_pin = account.pin
            response.session_key = account.new_session_key()
            response.init_capital = account.capital
            self.logger.info("id %s login success with session key %s" % (account.id, account.session_key))
        else:
            response.success = False
            if account is None:
                response.reason = "account id %d not found" % request.user_id
            else:
                response.reason = "account id and pin not match"
        return response

    def submit_answer(self, request: pb2.AnswerRequest, context):
        req = {
            "user_id": request.user_id,
            "user_pin": request.user_pin,
            "session_key": request.session_key,
            "sequence": request.sequence,
            "invest_ratio": request.invest_ratio[:],
            "timestamp": time.time()
        }

        response = pb2.AnswerResponse()
        response.accepted = True
        accepted, reason = self.validate_answer(req)
        self.logger.info(" %s submit_answer %s %s %s" % (context.peer(), req, accepted, reason))
        if accepted:
            self.answers.append(req)
        else:
            response.accepted = False
            response.reason = reason
        return response

    # Internal functions
    def validate_answer(self, req):
        if req is None or not req["invest_ratio"] or len(req["invest_ratio"]) != 4:
            return False, "request format error"
        account = self.account_manager.get_account(req["user_id"])
        if account is None:
            return False, "account id %s not found" % req["user_id"]
        if req["user_pin"] is None or req["user_pin"] != account.pin:
            return False, "pin not correct"
        if req["session_key"] is None or req["session_key"] != account.session_key:
            return False, "session key not match"
        if account.is_time_penalty:
            return False, "account under time penalty"

        local_question = self.current_question
        if local_question is None or local_question["sequence"] != req["sequence"]:
            return False, "answer timeout"

        if not sum(map(abs, req["invest_ratio"])) < 1 + 1e-6:
            return False, "invalid answer"
        return True, None
