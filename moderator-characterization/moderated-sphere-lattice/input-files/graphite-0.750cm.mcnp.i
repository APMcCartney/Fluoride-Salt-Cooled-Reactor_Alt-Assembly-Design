Uranium Marble - Graphite - 3.96480678186 cm cube lattice
C 
C 
C Cell Cards
C ----------------
C j	m	d	            geom	params
  1     1      -19.1                  -1        imp:n=1
  2     2      -1.69            1 -2     imp:n=1
999     0                              2        imp:n=0

C Surface Cards
C ------------------
C j	a	list
  1     so      1.23240339093
 *2     box     -1.98240339093 -1.98240339093 -1.98240339093 $ rear left lower corner
                3.96480678186 0.0000 0.0000
                0.0000 3.96480678186 0.0000
                0.0000 0.0000 3.96480678186

C Data Cards
C ------------------
C + mn - Material Cards
C ---------------------------
C Material 1 - Enriched Uranium Metal
m1    92235 -0.05   $ U235, 5% by mass
      92235 -0.95   $ U238, 95% by mass 
C 
C Material 2 - Graphite
m2   6000   1   $ Elemental Carbon
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
