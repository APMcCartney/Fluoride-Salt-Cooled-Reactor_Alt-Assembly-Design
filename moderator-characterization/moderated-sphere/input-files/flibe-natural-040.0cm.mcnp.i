Moderator Qualification - Uranium Marble - FLiBe w/ Natural Li - 040.0 cm
C 
C 
C Cell Cards
C ----------------
C j	m	d	            geom	params
  1     1      -19.1                  -1        imp:n=1
  2     2      -2.1228808                1 -2        imp:n=1
999     0                              2        imp:n=0

C Surface Cards
C ------------------
C j	a	list
  1     so      1.23240339093
  2     so      41.2324033909

C Data Cards
C ------------------
C + mn - Material Cards
C ---------------------------
C Material 1 - Enriched Uranium Metal
m1    92235 -0.05   $ U235, 5% by mass
      92235 -0.95   $ U238, 95% by mass 
C 
C Material 2 - FLiBe w/ Natural Li
m2   3006   0.15   $ Elemental Lithium \n     3007   1.85                       \n     4009   1   $ Elemental Beryllium \n     9019   4   $ Elemental Fluorine
C 
C ------------------
C + ksrc - Initial Fission Source Card
C ---------------------------
ksrc 0 0 0
C 
C ------------------
C + kcode - Criticality Card
C ---------------------------
kcode 75000 0.5 50 150
