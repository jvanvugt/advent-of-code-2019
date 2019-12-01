calcFuel :: Integer -> Integer
calcFuel mass = div mass 3 - 2

calcFuelBetter :: Integer -> Integer
calcFuelBetter mass = if extraFuel == 0 then 0 else extraFuel + calcFuelBetter extraFuel
    where extraFuel = max (calcFuel mass) 0

main = do
    f <- readFile "input01.txt"
    print $ sum $ map (calcFuelBetter . read) $ lines f
