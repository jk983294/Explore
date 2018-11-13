#!/usr/bin/env bash
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./contest/protos --python_out=./contest/_pyprotos --grpc_python_out=./contest/_pyprotos ./contest/protos/common.proto
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./contest/protos --python_out=./contest/_pyprotos --grpc_python_out=./contest/_pyprotos ./contest/protos/question.proto
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./contest/protos --python_out=./contest/_pyprotos --grpc_python_out=./contest/_pyprotos ./contest/protos/contest.proto


/opt/anaconda3/bin/python -m contest.server.server_main etc/server.xml
/opt/anaconda3/bin/python -m contest.client.client_main etc/client.xml
/opt/anaconda3/bin/python -m contest.client.multi_client_main etc/multi_clients.xml

/opt/anaconda3/bin/python -m contest.server.InitCapitalCalc /tmp/contest.users 20181030.153000 1000 /tmp/contest.init.capital

/opt/anaconda3/bin/python contest/server/PostClient.py
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'finish_test' '{"user_id": 1}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'undo_finish_test' '{"user_id": 1}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'penalty' '{"user_id": 1, "penalty_type": "time", "status": true}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'penalty' '{"user_id": 1, "penalty_type": "time", "status": false}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'penalty' '{"user_id": 1, "penalty_type": "money", "status": true}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'penalty' '{"user_id": 1, "penalty_type": "money", "status": false}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'admin' '{"cmd": "pause"}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'admin' '{"cmd": "resume"}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'admin' '{"cmd": "penalty", "user_id": 1, "money": 100}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'admin' '{"cmd": "dump_user", "path": "/tmp/contest.users"}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'admin' '{"cmd": "load_user", "path": "/tmp/contest.users"}'
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'admin' '{"cmd": "add_user", "user_name": "test", "user_id": 8888, "user_pin": "8888"}'


# final
/opt/anaconda3/bin/python -m contest.server.server_main etc/server_test.xml
/opt/anaconda3/bin/python contest/server/PostClient.py localhost 56703 'admin' '{"cmd": "dump_user", "path": "/tmp/contest.final.users"}'
/opt/anaconda3/bin/python -m contest.server.InitCapitalCalc /tmp/contest.final.users 20181104.143000 10000 /tmp/contest.final.init.capital
/opt/anaconda3/bin/python -m contest.server.server_main etc/server_final.xml
