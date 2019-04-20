protoc -I./contest/protos --grpc_out=./contest/cpp_client --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./contest/protos/common.proto
protoc -I./contest/protos --grpc_out=./contest/cpp_client --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./contest/protos/question.proto
protoc -I./contest/protos --grpc_out=./contest/cpp_client --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./contest/protos/contest.proto
protoc -I./contest/protos --cpp_out=./contest/cpp_client ./contest/protos/common.proto
protoc -I./contest/protos --cpp_out=./contest/cpp_client ./contest/protos/question.proto
protoc -I./contest/protos --cpp_out=./contest/cpp_client ./contest/protos/contest.proto

psg client_main | awk '{print $2}' | xargs kill
