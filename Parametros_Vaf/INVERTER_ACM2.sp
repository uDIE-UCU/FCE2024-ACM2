
VIN IN 0 PULSE(0 1.8 100n 10n 10n 100n 200n ) 
VBAT VDD 0 DC 1.8

N1 VDD IN OUT VDD PMOS_ACM W=1u L=1u n=1.3 IS=5u VT0=0.5 sigma=20m zeta=20m
N2 OUT IN 0 0 NMOS_ACM W=1u L=1u n=1.3 IS=5u VT0=0.5 sigma=20m zeta=20m

* model definitions:
.model NMOS_ACM nmos_ACM
.model PMOS_ACM pmos_ACM


.control
pre_osdi NMOS_ACM_2V0.osdi
pre_osdi PMOS_ACM_2V0.osdi
tran 1n 600n
plot V(OUT) V(IN)
.endc

.end