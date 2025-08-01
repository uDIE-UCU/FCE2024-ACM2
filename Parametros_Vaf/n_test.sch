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
N 30 60 90 60 {
lab=GND}
N -20 -90 -20 -80 {
lab=Vg}
N -20 50 -20 60 {
lab=GND}
N -20 -20 -20 -10 {
lab=Vs}
N 90 20 90 60 {
lab=GND}
N -70 -90 -20 -90 {
lab=Vg}
N -70 -90 -70 -50 {
lab=Vg}
N -70 -50 -60 -50 {
lab=Vg}
N -20 -110 -20 -90 {
lab=Vg}
N -20 -180 -20 -170 {
lab=#net1}
N -20 -180 90 -180 {
lab=#net1}
N 90 -180 90 -40 {
lab=#net1}
N -10 -20 30 -20 {
lab=GND}
N 30 -20 30 60 {
lab=GND}
N -20 60 30 60 {
lab=GND}
N -50 -10 -20 -10 {
lab=Vs}
C {vsource.sym} -20 20 0 0 {name=V1 value=\{vs\} savecurrent=false}
C {vsource.sym} 90 -10 0 0 {name=V2 value=\{Vdd\} savecurrent=false}
C {netlist_not_shown.sym} 170 -150 0 0 {name=s1 only_toplevel=false 
value="
* Circuit Parameters
.param vs = 3
.param step = 0.01
.param Vdd = 1.8
.param is = 0.173u
.param w = 5.0u
.param l = 0.18u
* Include Models
.model NMOS_ACM nmos_ACM
.model PMOS_ACM pmos_ACM
* OP Parameters & Singals to save
.save all
*Simulations
.dc V1 -1 \{vs\} \{step\}
.control
pre_osdi NMOS_ACM_2V0.osdi
pre_osdi PMOS_ACM_2V0.osdi
run
setplot dc1
plot v(Vg)
set filetype = ascii
write dcsweep.raw
.endc
.end
"}
C {lab_pin.sym} -70 -50 0 0 {name=p2 sig_type=std_logic lab=Vg}
C {gnd.sym} -20 60 0 0 {name=l1 lab=GND}
C {isource.sym} -20 -140 0 0 {name=I0 value=\{is\}}
C {lab_pin.sym} -50 -10 0 0 {name=p1 sig_type=std_logic lab=Vs}
C {nmos4.sym} -40 -50 0 0 {name=N1 model=NMOS_ACM w=\{w\} l=\{l\} del=0 m=1}
