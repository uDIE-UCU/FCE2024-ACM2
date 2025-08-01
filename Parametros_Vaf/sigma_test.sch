v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -80 -10 -70 -10 {
lab=GND}
N -80 -10 -80 20 {
lab=GND}
N -80 20 -70 20 {
lab=GND}
N -70 70 50 70 {
lab=GND}
N -70 -50 -70 -40 {
lab=Vd}
N -70 20 -70 70 {
lab=GND}
N -20 -10 -10 -10 {
lab=Vg}
N 50 -10 50 70 {
lab=GND}
N -70 -50 -0 -50 {
lab=Vd}
N -70 -70 -70 -50 {
lab=Vd}
N -70 -140 -70 -130 {
lab=Vdd}
N 40 -50 90 -50 {
lab=#net1}
N -20 -40 -20 -10 {
lab=Vg}
N -30 -10 -20 -10 {
lab=Vg}
N 90 50 90 70 {
lab=GND}
N 50 70 90 70 {
lab=GND}
N 90 -50 90 -10 {
lab=#net1}
N -140 -150 -140 -140 {
lab=Vdd}
N -140 50 -140 70 {
lab=GND}
N -140 70 -70 70 {
lab=GND}
N -140 -140 -140 -10 {
lab=Vdd}
N -140 -140 -70 -140 {
lab=Vdd}
C {netlist_not_shown.sym} 190 -110 0 0 {name=s1 only_toplevel=false 
value="
* Circuit Parameters
.param vd = 3
.param vdd = 1.2
.param step = 0.01
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
C {nmos4.sym} -50 -10 0 1 {name=N1 model=NMOS_ACM w=\{w\} l=\{l\} del=0 m=1}
C {lab_pin.sym} -70 -50 0 0 {name=p1 sig_type=std_logic lab=Vd}
C {lab_pin.sym} -20 -40 0 0 {name=p2 sig_type=std_logic lab=Vg}
C {gnd.sym} -70 70 0 0 {name=l1 lab=GND}
C {vcvs.sym} 20 -10 3 1 {name=E1 value=100}
C {isource.sym} -70 -100 0 0 {name=I0 value=1m}
C {lab_pin.sym} -140 -150 0 0 {name=p3 sig_type=std_logic lab=Vdd}
C {vsource.sym} 90 20 0 0 {name=V1 value=3 savecurrent=false}
C {vsource.sym} -140 20 0 0 {name=V2 value=\{vdd\} savecurrent=false}
