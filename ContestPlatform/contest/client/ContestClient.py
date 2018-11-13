import grpc
from .._pyprotos.contest_pb2_grpc import ContestStub
from .._pyprotos import contest_pb2 as pb2
from collections import deque
import time


class ContestClient:
    def __init__(self, contest_endpoint=None):
        if contest_endpoint:
            self._contest = ContestStub(grpc.insecure_channel(contest_endpoint))
        else:
            raise ValueError('Endpoint and Stub cannot both be None.')

        self.user_id = None
        self.user_pin = None
        self.session_key = None
        self.answers = deque(maxlen=2000)

    def login(self, user_id, user_pin):
        if user_id and user_pin:
            while True:
                try:
                    request = pb2.LoginRequest()
                    request.user_id = user_id
                    request.user_pin = user_pin
                    response = self._contest.login(request)

                    if response:
                        if response.success:
                            self.user_id = user_id
                            self.user_pin = user_pin
                            self.session_key = response.session_key
                            return True, None, response.init_capital, response.session_key
                        else:
                            return False, response.reason, 0, None
                except grpc.RpcError as error:
                    print('login failed. will retry one second later')
                    time.sleep(1)
        else:
            return False, "need id and pin to login", 0, None

    # Internal helper functions.
    def submit_answer(self, sequence, invest_ratio):
        try:
            request = pb2.AnswerRequest()
            request.user_id = self.user_id
            request.user_pin = self.user_pin
            request.session_key = self.session_key
            request.sequence = sequence
            request.invest_ratio.extend(invest_ratio)
            response = self._contest.submit_answer(request)
            return {"accepted": response.accepted, "reason": response.reason}
        except grpc.RpcError as error:
            return {"accepted": False, "reason": 'answer submit failed. (%s)' % str(error)}
