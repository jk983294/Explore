#include <grpc++/grpc++.h>
#include <unistd.h>
#include <cstdint>
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include "common.grpc.pb.h"
#include "contest.grpc.pb.h"
#include "question.grpc.pb.h"

using namespace std;
using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

struct QuestionClient {
    QuestionClient(std::shared_ptr<Channel> channel) : stub_(Question::NewStub(channel)) {}

    void get_question(int32_t user_id, int64_t sequence, QuestionResponse& response) {
        // Data we are sending to the server.
        QuestionRequest request;
        request.set_user_id(user_id);
        request.set_sequence(sequence);

        // Context for the client. It could be used to convey extra information to
        // the server and/or tweak certain RPC behaviors.
        ClientContext context;

        while (true) {
            Status status = stub_->get_question(&context, request, &response);

            if (status.ok()) {
                return;
            }
        }
    }

    std::unique_ptr<Question::Stub> stub_;
};

struct ContestClient {
    ContestClient(std::shared_ptr<Channel> channel) : stub_(Contest::NewStub(channel)) {}

    UserLoginResponse login(int32_t user_id, string user_pin) {
        LoginRequest request;
        request.set_user_id(user_id);
        request.set_user_pin(user_pin);

        UserLoginResponse reply;
        ClientContext context;

        while (true) {
            Status status = stub_->login(&context, request, &reply);

            if (status.ok()) {
                return reply;
            }
        }
    }

    void submit_answer(const AnswerRequest& request, AnswerResponse& response) {
        ClientContext context;
        while (true) {
            Status status = stub_->submit_answer(&context, request, &response);
            if (status.ok()) {
                return;
            }
        }
    }

    std::unique_ptr<Contest::Stub> stub_;
};

void get_payoffs(const QuestionResponse& questionResponse, vector<vector<double>>& payoffs) {
    int size = questionResponse.payoffs_size();
    payoffs.clear();
    payoffs.resize(size);
    for (int i = 0; i < size; ++i) {
        auto& arr = questionResponse.payoffs(i);
        for (int j = 0; j < size; ++j) {
            payoffs[i].push_back(arr.values(j));
        }
    }
}

void get_price_distribution(const QuestionResponse& questionResponse, vector<double>& price_distribution) {
    price_distribution.clear();
    int size = questionResponse.price_distribution().values_size();
    for (int i = 0; i < size; ++i) {
        price_distribution.push_back(questionResponse.price_distribution().values(i));
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "./client_main <id> <pin>" << endl;
        return -1;
    }
    int32_t id = std::atoi(argv[1]);
    string pin{argv[2]};

    QuestionClient questionClient(grpc::CreateChannel("localhost:56701", grpc::InsecureChannelCredentials()));
    ContestClient contestClient(grpc::CreateChannel("localhost:56702", grpc::InsecureChannelCredentials()));
    UserLoginResponse loginResponse = contestClient.login(id, pin);
    string session_key;
    if (loginResponse.success()) {
        session_key = loginResponse.session_key();
    } else {
        cout << "login failed due to " << loginResponse.reason() << endl;
        return -1;
    }

    int64_t seq = 0;
    vector<vector<double>> payoffs;
    vector<double> price_distribution;
    QuestionResponse questionResponse;
    AnswerRequest answerRequest;
    answerRequest.set_user_id(id);
    answerRequest.set_user_pin(pin);
    answerRequest.set_session_key(session_key);
    AnswerResponse answerResponse;
    while (true) {
        while (true) {
            questionClient.get_question(id, seq, questionResponse);
            if (questionResponse.sequence() == -1) {
                // cout << "question for seq " << seq << " not ready" << endl;
                usleep(100 * 1000);  // 0.1s
            } else {
                seq = questionResponse.sequence();
                // cout << "question for seq " << seq << " ready" << endl;
                break;
            }
        }

        get_payoffs(questionResponse, payoffs);
        get_price_distribution(questionResponse, price_distribution);

        answerRequest.set_sequence(seq);
        answerRequest.clear_invest_ratio();
        answerRequest.add_invest_ratio(0.25);
        answerRequest.add_invest_ratio(0.25);
        answerRequest.add_invest_ratio(0.25);
        answerRequest.add_invest_ratio(0.25);

        contestClient.submit_answer(answerRequest, answerResponse);
        if (answerResponse.accepted()) {
            cout << "answer accepted" << endl;
        } else {
            cout << "answer failed to accept due to" << answerResponse.reason() << endl;
        }
        ++seq;
    }
    return 0;
}
