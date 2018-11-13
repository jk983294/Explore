from .._pyprotos import question_pb2 as pb2, question_pb2_grpc as pb2_grpc
from .._pyprotos import common_pb2
import grpc
from concurrent import futures
from collections import deque
import time
import threading
from .GameRule import get_stock_distribution, get_payoffs
import json


class QuestionPublisher(pb2_grpc.QuestionServicer):
    def __init__(self, port, round_, global_info=None):
        self._is_started = False
        self._is_paused = False
        self._update_interval = global_info.update_interval  # seconds
        self.total_round = round_
        self.sequence = 0
        self.current_question = None
        self.questions = deque(maxlen=2000)
        self.global_info = global_info
        self.account_manager = global_info.accountManager
        self.game_engine = global_info.game_engine
        self.answer_service = global_info.answer_service
        self.mode = global_info.mode
        self.logger = global_info.logger

        # gRPC server
        self._server = None
        self._port = port

        self._updater = threading.Thread(target=self._generate_question)

    def start(self):
        if self._is_started:
            raise NotImplementedError

        self._is_started = True
        self._updater.start()

        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_QuestionServicer_to_server(self, self._server)

        self._server.add_insecure_port('[::]:%d' % self._port)
        self._server.start()

    def stop(self):
        if not self._is_started:
            raise NotImplementedError

        # Stops publishing and prevents new subscriptions
        self._is_started = False

        if self._server:
            self._server.stop(0).wait()
            del self._server
            self._server = None

    def pause_publish(self):
        if self._is_paused:
            return False, "already paused"
        self._is_paused = True
        return True, "pause success"

    def resume_publish(self):
        if not self._is_paused:
            return False, "still running"
        self._is_paused = False
        return True, "resume success"

    # API:

    def get_question(self, request: pb2.QuestionRequest, context=None):
        user_id = request.user_id
        seq = request.sequence
        if self._is_started:
            return self._get_response(user_id, seq)

    # Internal functions

    def _generate_question(self):
        while self._is_started:
            time.sleep(self._update_interval)
            self.sequence += 1
            distribution = self.game_engine.get_stock_distribution()
            payoffs = self.game_engine.get_payoffs(distribution)

            has_next_question = True
            if self.total_round is not None and self.total_round > 0 and self.sequence >= self.total_round:
                has_next_question = False
            self.current_question = {
                "sequence": self.sequence,
                "distribution": distribution,
                "payoffs": payoffs,
                "timestamp": time.time(),
                "has_next_question": has_next_question
            }

            self.answer_service.current_question = self.current_question

            self.questions.append(self.current_question)
            self.logger.info("new question %s" % json.dumps(self.current_question))
            # print("current_question", self.current_question)
            if not has_next_question:
                break
            while self._is_paused:
                print("question publisher paused")
                time.sleep(1)
        print("total %d questions published" % self.sequence)

    def _get_response(self, user_id, seq):
        """Creates a MarketSnapshot response with latest instrument snapshots."""
        response = pb2.QuestionResponse()
        response.sequence = -1          # means error
        if seq is not None and seq <= self.sequence and self.current_question:
            local_question = self.current_question
            response.user_id = user_id
            response.sequence = local_question["sequence"]
            response.has_next_question = local_question["has_next_question"]
            account = self.account_manager.get_account(user_id)
            if account:
                response.capital = account.capital
            else:
                response.capital = -1.0
            response.price_distribution.values.extend(local_question["distribution"])
            for payoff in local_question["payoffs"]:
                payoffs = response.payoffs.add()
                payoffs.values.extend(payoff)
        else:
            time.sleep(0.1)
        return response
