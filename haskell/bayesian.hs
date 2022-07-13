import qualified Data.List as L
import qualified Data.Map as M

data BayesNet  = BayesNet{
                             node :: [String],
                             edge :: [(String,String)]
                          } deriving(Show,Eq)

data Item      = Item{
                          name :: String,
                          proba :: [(String,Double)]
                      } deriving(Show,Eq)


{-
  query parent of node
-}
type Table = [Item]

queryParent :: BayesNet  -> String -> [String]
queryParent (BayesNet _ edges) n = [fst x | x <- edges,snd x == n]

frequence :: (Ord a) => [a] -> [(a,Double)]
frequence xs = M.toList $  M.fromListWith (+) [(x, 1.0) | x <- xs];

fromList2Item :: String -> [String] -> Item
fromList2Item n ns = Item n (proba ns)
  where proba xs   = let frequence_list = frequence xs;
                         l              = fromIntegral $ length  xs in
                         map (\x -> (fst x,(snd x) / l)) frequence_list

