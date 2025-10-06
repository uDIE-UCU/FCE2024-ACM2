v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -20 -50 -10 -50 {
lab=GND}
N -10 -50 -10 -20 {
lab=GND}
N -20 -20 -10 -20 {
lab=GND}
N -20 -20 -20 30 {
lab=GND}
N -130 30 -20 30 {
lab=GND}
N -130 20 -130 30 {
lab=GND}
N -20 30 90 30 {
lab=GND}
N 90 20 90 30 {
lab=GND}
N -130 -50 -60 -50 {
lab=Vg}
N -130 -50 -130 -40 {
lab=Vg}
N -20 -90 -20 -80 {
lab=Vd}
N -20 -90 90 -90 {
lab=Vd}
N 90 -90 90 -40 {
lab=Vd}
N 90 -120 90 -90 {
lab=Vd}
N -130 -70 -130 -50 {
lab=Vg}
C {vsource.sym} -130 -10 0 0 {name=V1 value=\{Vg\} savecurrent=false}
C {vsource.sym} 90 -10 0 0 {name=V2 value=DC(\{phi_t*0.5\}) savecurrent=false}
C {netlist_not_shown.sym} 170 -150 0 0 {name=s1 only_toplevel=false 
value="
* Circuit Parameters
.param vg = 3
.param step = 0.01
.param phi_t = 0.0258
.param w = 5.0u
.param l = 0.18u
* Include Models
.lib /opt/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib /opt/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOShv.lib mos_tt
* OP Parameters & Singals to save
.save all
*Simulations
.dc V1 0 \{vg\} \{step\}
.control
run
setplot dc1
plot -i(V2)
set filetype = ascii
write dcsweep.raw
.endc
.end
"}
C {lab_pin.sym} 90 -120 0 0 {name=p1 sig_type=std_logic lab=Vd}
C {lab_pin.sym} -130 -70 0 0 {name=p2 sig_type=std_logic lab=Vg}
C {gnd.sym} -20 30 0 0 {name=l1 lab=GND}
C {sg13g2_pr/sg13_lv_nmos.sym} -40 -50 2 1 {name=M1
l=\{l\}
w=\{w\}
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
