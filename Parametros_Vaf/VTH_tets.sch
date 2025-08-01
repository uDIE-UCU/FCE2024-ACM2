v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -70 -10 -60 -10 {
lab=GND}
N -60 -10 -60 20 {
lab=GND}
N -70 20 -60 20 {
lab=GND}
N -70 20 -70 70 {
lab=GND}
N -180 70 -70 70 {
lab=GND}
N -180 60 -180 70 {
lab=GND}
N -70 70 40 70 {
lab=GND}
N 40 60 40 70 {
lab=GND}
N -180 -10 -110 -10 {
lab=Vg}
N -180 -10 -180 0 {
lab=Vg}
N -70 -50 -70 -40 {
lab=Vd}
N -70 -50 40 -50 {
lab=Vd}
N 40 -50 40 0 {
lab=Vd}
N 40 -80 40 -50 {
lab=Vd}
N -180 -30 -180 -10 {
lab=Vg}
C {netlist_not_shown.sym} 190 -110 0 0 {name=s1 only_toplevel=false 
value="
* Circuit Parameters
.param vg = 3
.param step = 0.01
.param phi_t = 0.0258
.param w = 5.0u
.param l = 0.18u
* Include Models
.model NMOS_ACM nmos_ACM
.model PMOS_ACM pmos_ACM
* OP Parameters & Singals to save
.save all
*Simulations
.dc V1 0 \{vg\} \{step\}
.control
pre_osdi NMOS_ACM_2V0.osdi
pre_osdi PMOS_ACM_2V0.osdi
run
let gm_id = deriv(-1*i(V2))/(-1*i(V2))
setplot dc1
plot gm_id
set filetype = ascii
write dcsweep.raw
.endc
.end
"}
C {nmos4.sym} -90 -10 0 0 {name=N1 model=NMOS_ACM w=\{w\} l=\{l\} del=0 m=1}
C {vsource.sym} -180 30 0 0 {name=V1 value=\{Vg\} savecurrent=false}
C {vsource.sym} 40 30 0 0 {name=V2 value=DC(\{phi_t*0.5\}) savecurrent=false}
C {lab_pin.sym} 40 -80 0 0 {name=p1 sig_type=std_logic lab=Vd}
C {lab_pin.sym} -180 -30 0 0 {name=p2 sig_type=std_logic lab=Vg}
C {gnd.sym} -70 70 0 0 {name=l1 lab=GND}
