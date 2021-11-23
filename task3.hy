(import [generation_maze [maze]]
        [minimax [FieldState]]
        [tree_building [tree_build]])


(setv matrix (maze 5 5 (, 0 2) [(, 3 2)]))
(setv field (FieldState matrix))
(setv tree (tree_build field (, 4 1) 2))
(print tree)