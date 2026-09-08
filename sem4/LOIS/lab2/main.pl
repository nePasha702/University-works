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

% 1. Начальное состояние (твоя исходная конфигурация)
initial_state([0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]).

% 2. Целевое состояние
target_state([0, 0, 0, N4, N5, N6, 0, 0, 0, N10, 0, 0, 0]) :-
    member(N4, [0, 1]), member(N5, [0, 1]), member(N6, [0, 1]), member(N10, [0, 1]),
    Sum is N4 + N5 + N6 + N10,
    Sum =:= 3.

% 3. Правила переходов
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

% 4. Главный предикат поиска (IDDFS)
solve(Moves) :-
    initial_state(Init),
    target_state(Target),
    length(Moves, _),
    solve_path(Init, Target, Moves, [Init]).

solve_path(Target, Target, [], _Visited).

solve_path(Current, Target, [Move | RestMoves], Visited) :-
    move(Current, Move, Next),
    \+ member(Next, Visited),
    solve_path(Next, Target, RestMoves, [Next | Visited]).

% Точка входа
begin :-
    writeln('--- Поиск оптимального пути (IDDFS) ---'),
    ( solve(Path) ->
        writeln('Кратчайший путь найден:'),
        maplist(writeln, Path)
    ;
        writeln('Решение не найдено.')
    ).