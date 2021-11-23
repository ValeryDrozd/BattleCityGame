(import [pandas :as pd]
        math
)

(defn square[num]
    (math.pow num 2)
)

(setv dataset (pd.read_csv "./output1.csv"))
(setv time (get dataset "time"))
(setv points (get dataset "points"))

(defn expectation[col]
    (/ (col.sum) (len col))
) 

(defn dispersion[col]
    ( - (expectation (col.map square) ) (square (expectation col)) 
)) 

(print (+ "Math Expectation on time: " (str (expectation time))))

(print (+ "Dispersion on points: " (str (dispersion points))))
