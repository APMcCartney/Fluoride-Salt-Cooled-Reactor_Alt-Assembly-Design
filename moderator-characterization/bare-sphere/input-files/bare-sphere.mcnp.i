Moderator Qualification - Bare Uranium Marble - 1 fast neutron mfp diameter
C
C Cell Cards
C ------------------
C j	m	d	geom	params
  1     1     -19.1      -1     imp:n=1
 999    0                 1     imp:n=0

C Surface Cards
C ------------------
C j	a	list
  1     so      1.23240339093  $ Surface of the uranium metal marble
C                                Surface label: 1
C                                Surface type: sphere centered at the origin
C                                Defining values: 1.23 cm radius (~ 0.5 fast mfp)

C Data Cards
C ------------------
C + mn - Material Cards
C ---------------------------
C 
C Material 1 - Enriched Uranium Metal
m1    92235 -0.05   $ U235, 5% by mass
      92238 -0.95   $ U238, 95% by mass 
C 
C ------------------
C + ksrc - Initial Fission Source Card
C ---------------------------
ksrc 0 0 0
C 
C ------------------
C + kcode - Criticality Card
C ---------------------------
kcode 50000 0.5 50 250