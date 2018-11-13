import grpc
from .._pyprotos.question_pb2_grpc import QuestionStub
from .._pyprotos import question_pb2 as pb2
import threading
import time
from collections import deque


class QuestionClient:
    def __init__(self, question_endpoint=None, user_id=None):
        if question_endpoint:
            self._question = QuestionStub(grpc.insecure_channel(question_endpoint))
        else:
            raise ValueError('Endpoint cannot be None.')

        self._is_started = True
        self.user_id = user_id
        self.sequence = 0
        self.current_question = None
        self.questions = deque(maxlen=2000)

        self._updater = None
        try:
            self._updater = threading.Thread(target=self._update_question)
            self._updater.start()
        except grpc.RpcError as error:
            print('RPC error:', str(error))
            print('server disconnected.')

    def __del__(self):
        self._is_started = False

    # Internal helper functions.
    def _update_question(self):
        while self._is_started:
            try:
                request = pb2.QuestionRequest()
                request.user_id = self.user_id
                request.sequence = self.sequence
                response = self._question.get_question(request)

                if response.sequence == -1:
                    time.sleep(0.5)
                    continue

                if response.has_next_question is False:
                    print("get last question")
                    self._is_started = False

                ret = {
                    "user_id": response.user_id,
                    "sequence": response.sequence,
                    "capital": response.capital,
                    "has_next_question": response.has_next_question,
                    "price_distribution": response.price_distribution.values[:],
                    "payoffs": [payoff.values[:] for payoff in response.payoffs]
                }
                self.questions.append(ret)
                if response.sequence >= self.sequence:
                    self.sequence = response.sequence + 1
                    time.sleep(4)
                else:
                    time.sleep(0.5)
            except grpc.RpcError as error:
                print('question updater stopped. (%s)' % str(error))
                time.sleep(1)

        print("finish get all questions")

    def get_question(self):
        has_next = True
        while has_next:
            if self.questions:
                q = self.questions.popleft()
                if not q["has_next_question"]:
                    has_next = False
                yield q
            else:
                time.sleep(0.1)
