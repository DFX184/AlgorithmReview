import qualified Data.List as L

data Atom  = Atom {
                      content :: [Char],
                      logic   :: Bool 
                   } deriving(Show)

{-
  Basic Operator of logic
-}

cand :: Atom  -> Atom  -> Atom 
cand (Atom lc  l) (Atom rc r) = Atom (" ( " ++ lc ++ " and " ++ rc ++ " ) " ) (l && r)

(-|) :: Atom  -> Atom  -> Atom

(-|) (Atom lc l) (Atom rc r) = Atom (" ( " ++ lc  ++ " or " ++  rc ++ " ) ") (l || r)

(*->) :: Atom -> Atom -> Atom

(*->) (Atom lc True) (Atom rc  False) = Atom (" ( " ++  lc ++ " imply " ++ rc ++ " ) ")  False
(*->) (Atom lc _) (Atom rc _)         = Atom (" ( " ++ lc ++ " imply " ++ rc ++ " ) ")  True 

(<->) :: Atom -> Atom -> Atom
(<->) (Atom lc l) (Atom rc r ) = Atom (lc ++ " iff " ++  rc) (l == r)

{-
  Table value 
-}


