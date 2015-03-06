Moderator Qualification - Uranium Marble - $(description) - $(radius) cm
C 
C $py(import pickle; )
C 
C Cell Cards
C ----------------
C j	m	d	            geom	params
  1     1      -19.1                  -1        imp:n=1
  2     2      $(moderator_density)                1 -2        imp:n=1
999     0                              2        imp:n=0

C Surface Cards
C ------------------
C j	a	list
  1     so      $(1.23240339093)
  2     so      $(1.23240339093 + float(radius)))

C Data Cards
C ------------------
C + mn - Material Cards
C ---------------------------
C Material 1 - Enriched Uranium Metal
m1    92235 -0.05   \$ U235, 5% by mass
      92235 -0.95   \$ U238, 95% by mass 
C 
C Material 2 - $(moderator_label)
$(moderator_material_card)
C 
C ------------------
C + ksrc - Initial Fission Source Card
C ---------------------------
ksrc 0 0 0
C 
C ------------------
C + kcode - Criticality Card
C ---------------------------
kcode $(particles_per_cycle) $(criticality_guess) $(skipped_cycles) $(total_cycles)
