Moderator Qualification - Uranium Marble - Graphite - 004.0 cm
C 
C 
C Cell Cards
C ----------------
C j	m	d	            geom	params
  1     1      -19.1                  -1        imp:n=1
  2     2      -1.69                1 -2        imp:n=1
999     0                              2        imp:n=0

C Surface Cards
C ------------------
C j	a	list
  1     so      1.23240339093
  2     so      5.23240339093

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
kcode 75000 0.5 50 150
