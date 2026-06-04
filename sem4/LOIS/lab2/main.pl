################################################################################
# Лабораторная работа №2 по дисциплине "ЛОИС"
# Выполнена студентом группы 421702 БГУИР Перервой Павлом Дмитриевичем
# Файл: main.pl - реализация алгоритма поиска в ширину для решения задачи о 3 сферах на 13 узлах.
# Дата: 03.06.2026
#
# Ссылки на использованные материалы:
# [1] Голенков, В. В. Логические основы интеллектуальных систем. Практикум.
# [2] https://www.swi-prolog.org/ - официальный сайт SWI-Prolog, использованного для реализации.
################################################################################
:- encoding(utf8).

target_state([_, _, _, N4, N5, N6, _, _, _, N10, _, _, _]) :-
    Sum is N4 + N5 + N6 + N10,
    Sum =:= 3.

move(State, rotate(c1, cw), NextState) :-
    State = [N1,N2,N3,N4,N5,N6, N7,N8,N9,N10,N11,N12,N13],
    NextState = [N6,N1,N2,N3,N4,N5, N7,N8,N9,N10,N11,N12,N13].

move(State, rotate(c1, ccw), NextState) :-
    State = [N1,N2,N3,N4,N5,N6, N7,N8,N9,N10,N11,N12,N13],
    NextState = [N2,N3,N4,N5,N6,N1, N7,N8,N9,N10,N11,N12,N13].

move(State, rotate(c2, cw), NextState) :-
    State = [N1,N2,N3,N4,N5,N6, N7,N8,N9,N10,N11,N12,N13],
    NextState = [N1,N2,N3,N7,N4,N6, N8,N9,N10,N5,N11,N12,N13].

move(State, rotate(c2, ccw), NextState) :-
    State = [N1,N2,N3,N4,N5,N6, N7,N8,N9,N10,N11,N12,N13],
    NextState = [N1,N2,N3,N5,N10,N6, N4,N7,N8,N9,N11,N12,N13].

move(State, rotate(c3, cw), NextState) :-
    State = [N1,N2,N3,N4,N5,N6, N7,N8,N9,N10,N11,N12,N13],
    NextState = [N1,N2,N3,N4,N6,N13, N7,N8,N9,N5,N10,N11,N12].

move(State, rotate(c3, ccw), NextState) :-
    State = [N1,N2,N3,N4,N5,N6, N7,N8,N9,N10,N11,N12,N13],
    NextState = [N1,N2,N3,N4,N10,N5, N7,N8,N9,N11,N12,N13,N6].

solve(InitialState, Path) :-
    bfs([[InitialState, []]], [], RevPath),
    reverse(RevPath, Path).

bfs([[CurrentState, Path] | _], _, Path) :-
    target_state(CurrentState), !.

bfs([[CurrentState, CurrentPath] | RestQueue], Visited, FinalPath) :-
    findall(
        [NextState, [Action | CurrentPath]],
        (
            move(CurrentState, Action, NextState),
            \+ member(NextState, Visited) % Проверка, что состояние не посещалось
        ),
        NewNodes
    ),
    append(RestQueue, NewNodes, NextQueue),
    bfs(NextQueue, [CurrentState | Visited], FinalPath).

begin :-
    Init = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    writeln('--- Поиск оптимального пути (BFS) ---'),
    ( solve(Init, Path) ->
        writeln('Кратчайший путь найден:'),
        maplist(writeln, Path)
    ;
        writeln('Решение не найдено.')
    ).