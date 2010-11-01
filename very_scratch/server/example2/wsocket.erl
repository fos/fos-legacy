-module(wsocket).
-compile(export_all).

start() ->
    F = fun interact/2,
    spawn(fun() -> start(F, 0) end).

interact(Browser, State) ->
    receive
        {browser, Browser, Str} ->
            Str1 = lists:reverse(Str),
            Browser ! {send, "out ! " ++ Str1},
            interact(Browser, State)
    after
        100 ->
            Browser ! {send, "clock ! tick" ++ integer_to_list(State)},
            interact(Browser, State+1)
    end.

start(F, State0) ->
    {ok, Listen} = gen_tcp:listen(1234, [{packet, 0},
                                            {reuseaddr, true},
                                            {active, true}]),
    par_connect(Listen, F, State0).

par_connect(Listen, F, State0) ->
    {ok, Socket} = gen_tcp:accept(Listen),
    spawn(fun() -> par_connect(Listen, F, State0) end),
    wait(Socket, F, State0).

wait(Socket, F, State0) ->
    receive
        {tcp, Socket, Data} ->
            io:format("Starting Handshake~n"),
            Handshake = ["HTTP/1.1 101 Web Socket Protocol Handshake\r\n",
            "Upgrade: WebSocket\r\n",
            "Connection: Upgrade\r\n",
            "WebSocket-Origin: http://localhost:8888\r\n",
            "WebSocket-Location: ",
            " ws://localhost:1234/websession\r\n\r\n"],
            io:format("Sending data~n"),
            gen_tcp:send(Socket, Handshake),
            S = self(),
            io:format("spawn_link~n"),
            Pid = spawn_link(fun() -> F(S, State0) end),
            io:format("recuring...~n"),
            loop(zero, Socket, Pid);
    Any ->
        io:format("Received~p~n", [Any]),
        wait(Socket, F, State0)
    end.

loop(Buff, Socket, Pid) ->
    receive
        {tcp, Socket, Data} ->
            io:format("loop:handle~n"),
            handle_data(Buff, Data, Socket, Pid);
        {tcp_closed, Socket} ->
            io:format("loop:tcp_closed~n"),
            Pid ! {browser_closed, self()};
        {send, Data} ->
            io:format("loop:send_data~n"),
            gen_tcp:send(Socket, [0, Data, 255]),
            io:format("loop:recur~n"),
            loop(Buff, Socket, Pid);
        Any ->
            io:format("Received~p~n", [Any]),
            loop(Buff, Socket, Pid)
    end.

handle_data(zero, [0|T], Socket, Pid) ->
    handle_data([], T, Socket, Pid);
handle_data(zero, [], Socket, Pid) ->
    loop(zero, Socket, Pid);
handle_data(L, [255|T], Socket, Pid) ->
    Line = lists:reverse(L),
    Pid ! {browser, self(), Line},
    handle_data(zero, T, Socket, Pid);
handle_data(L, [H|T], Socket, Pid) ->
    handle_data([H|L], T, Socket, Pid);
handle_data([], L, Socket, Pid) ->
    loop(L, Socket, Pid).