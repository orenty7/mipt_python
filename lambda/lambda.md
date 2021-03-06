### Как работают лямбда-функции:
Пусть `{x B}` это лямбда функция, где `B` -- какая-то строка.
Тогда при исполнении этой функции, например `{x B} y` во всех 
местах переменная `x` заменится на `y`
####Примеры:
    1. {x x} y => y, то есть {x x} = id x
    2. {x x x} "ab" => "ab" "ab"
    3. {x x x} {x x x} => {x x x} {x x x} -- бесконечный цикл
    4. {x {y x+y}} 10 20 => {y 10+y} 20 => 10+20
####Определение простейших объектов:
Для начала определеним булевы объекты. Будем считать, что лямбда-функция представляет
собой `true`, если она принимает два аргумента и возвращает первый из них.
То есть если это функция эквивалентная функции `{x {y x}}`. Аналогично будем считать, что
лямбда функция это `false`, если она эквивалентна `{x {y y}}`. Определим ветвления и логические
операции на булевых переменных. Начнём с операции ветвления. 

`if = {condition {true_block {false_block condition true_block false_block}}}`

Это функция от трёх аргументов. Она принимает на вход условие, ветку true и ветку false.
Ввиду определения значений `true` и `false`, исполнится ровно одна из ветвей, а вторая
отбросится. Определим на её основе логические операции:
- `not = if x (false) (true)`
- `and = if x y (false)`
- `or = if x (true) y`

Определим числа как функции вида `{s {z s (s (s...s z))...)}}`. Где количество применений функции s 
равно числу. То есть будем считать, что
- `0 = {s {z z}}`
- `1 = {s {z s z}}`
- `2 = {s {z s (s z)}}`
- `3 = {s {z s (s (s z))}}`**`...`**

Определим теперь операции на числах. Первой определим операцию `(+1)` это можно представить такой
функцией `(+1) = {x {s {z s (x s z)}}}}` Теперь определим сложение. Ввиду того как 
определены числа, сложение можно записать просто как `sum = m (+1) n`

