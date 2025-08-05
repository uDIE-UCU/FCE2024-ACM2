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
N -70 -50 -70 -40 {
lab=#net1}
N -130 -10 -130 -0 {
lab=Vdd}
N -130 -10 -110 -10 {
lab=Vdd}
N -130 -60 -130 -10 {
lab=Vdd}
N -130 70 -70 70 {
lab=GND}
N -130 60 -130 70 {
lab=GND}
C {netlist_not_shown.sym} 190 -110 0 0 {name=s1 only_toplevel=false 
value="
* Circuit Parameters
.param vdd = 1.2
.param w = 5.0u
.param l = 0.18u
* Include Models
.model NMOS_ACM nmos_ACM
.model PMOS_ACM pmos_ACM
* OP Parameters & Singals to save
.save all
*Simulations
.op
.control
pre_osdi NMOS_ACM_2V0.osdi
pre_osdi PMOS_ACM_2V0.osdi
run
print i(Vd)
set filetype = ascii
write dcsweep.raw
.endc
.end
"}
C {nmos4.sym} -90 -10 0 0 {name=N1 model=NMOS_ACM w=\{w\} l=\{l\} del=0 m=1}
C {vsource.sym} -130 30 0 0 {name=V2 value=\{vdd\} savecurrent=false}
C {lab_pin.sym} -130 -60 0 0 {name=p1 sig_type=std_logic lab=Vdd}
C {gnd.sym} -70 70 0 0 {name=l1 lab=GND}
C {ammeter.sym} -100 -50 3 1 {name=Vd savecurrent=true }
