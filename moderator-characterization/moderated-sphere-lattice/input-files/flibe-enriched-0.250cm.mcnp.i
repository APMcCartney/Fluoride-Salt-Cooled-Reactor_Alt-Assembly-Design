Uranium Marble - FLiBe w/ Enriched Li - 2.96480678186 cm cube lattice
C 
C 
C Cell Cards
C ----------------
C j	m	d	            geom	params
  1     1      -19.1                  -1        imp:n=1
  2     2      -2.1228808            1 -2     imp:n=1
999     0                              2        imp:n=0

C Surface Cards
C ------------------
C j	a	list
  1     so      1.23240339093
 *2     box     -1.48240339093 -1.48240339093 -1.48240339093 $ rear left lower corner
                2.96480678186 0.0000 0.0000
                0.0000 2.96480678186 0.0000
                0.0000 0.0000 2.96480678186

C Data Cards
C ------------------
C + mn - Material Cards
C ---------------------------
C Material 1 - Enriched Uranium Metal
m1    92235 -0.05   $ U235, 5% by mass
      92235 -0.95   $ U238, 95% by mass 
C 
C Material 2 - FLiBe w/ Enriched Li
m2   3006   0.001 $ Lithium-6 
     3007   1.999 $ Lithium-7 
     4009   1   $ Elemental Beryllium 
     9019   4   $ Elemental Fluorine
C 
C ------------------
C + ksrc - Initial Fission Source Card
C ---------------------------
ksrc 0 0 0
C 
C ------------------
C + kcode - Criticality Card
C ---------------------------
kcode 75000 1.2 10 50
