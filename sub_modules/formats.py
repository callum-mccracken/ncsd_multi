"""Holds big long strings to make writing files easier

note: double curly braces tell Python you mean a literal curly brace
      when you're formatting a string.
      "{a}, {b}, {{a}}".format(a=1, b=2) produces the string "1, 2, {a}"
"""

mfdp_format = """==== Input file for the shell model code ===== 
INT filename and output file name:
{two_body_interaction}
{two_body_file_type}     <- TBME file: a b c d  J T  Trel  Hrel  Clmb   V ...
{output_file}
  {Z}   {N}  {hbar_omega}   ! Z, N, hbar*Omega
  {Nhw}  {parity}  {total_2Mz}     !  Nhw  =  sum(2n+l),  Parity  (0  for  +,  1  for  -),  Total  2
  {N_min}  {N_1max}   {N_12max}   ! N_min,N_1max,N_12max
  {iham}  {iclmb}    {strcm}  ! iham(1: H=Trel+G, 2: H=Hrel+G, 3: H=SPE+G), iclmb, strcm
  {interaction_type}            ! For a 32-bit machine; nbits = 64 for a 64-bit machine
  {major}            ! major (0 for subshells, 1 for major shells)
  {nshll}            ! nshll/jorder (norb (major=0) OR orbital order)
Major or subshell occupation restrictions for protons, neutrons and (p+n):
{occupation_string}
Control parameters for multiple-G calculations:
  {nsets}  {min_nesp}  {nskip}  {iset1}   ! nsets (# of G's), min(nesp), nskip, iset1 (see below)
Control parameters for initial and final state vectors:
  {ki}  {kf}  {n_states}     ! ki,kf,nf (Initial, 1st final state, # of final states)
  {gs_energy}      ! the g.s. energy (0 if not available)
Other control parameters:
  {iterations_required}         ! Number of iterations required, minimum to do
  {igt}            ! igt = 1 to calculate sum GT+ and sum GT-, = 0 not to.
Restart option:
  {irest}           ! irest = 1 to restart, = 0 not to.
  {nhme}            ! Number of Ham matrix elements (nhme), used when irest=1
Importance truncation:
  {nhw0}  {nhw_min}  {Nhw}  {nhw_restart}  ! nhw0, nhw_min (start IT), nhw_max=nhw, nhw_restart
  {kappa_points}  {cmin}   {kappa_restart}  !kappa_points,cmin=factor*kappa,kappa_restart
 {kappa_vals}        ! kappa(1E-5)
  {convergence_delta}           ! convergence delta in keV
{three_body_interaction}
{N_1max} {N_12max} {N_123max}
Effective operators:
   {eff_charge_p:.3f}    {eff_charge_n:.3f}     <- effective charges: ep and en
   {glp:.3f}    {gln:.3f}    {gsp:.3f}   {gsn:.3f}   <- glp,gln,gsp,gsn
{saved_pivot}           ! saved_pivot
{rmemavail}        ! rmemavail
*******************************  End of input  *******************************
"""

batch_format = """#!/bin/bash
#SBATCH --account={account}
#SBATCH --ntasks={ntasks}               # number of MPI processes
#SBATCH --mem-per-cpu={mem_per_cpu}      # memory; default unit is megabytes
#SBATCH --time={time}           # time (DD-HH:MM)
#SBATCH --output={output}

cd {run_directory}

potential="{potential}"

iNu="{nucleus_name}"
freq="{hbar_omega}"
suf="{suffix}"
Ngs={Ngs}


srun {ncsd_path}

for Nmax in {non_IT_Nmax}

do

N=$[$Nmax+$Ngs]

mv mfdp_${{N}}.egv mfdp_${{N}}.egv_${{iNu}}_${{potential}}_Nmax${{Nmax}}.${{freq}}${{suf}}

done

for Nmax in {IT_Nmax}

do

N=$[$Nmax+$Ngs]

{kappa_rename}
done
"""

kappa_rename_format = """mv mfdp_${{N}}{kappa_D}.egv mfdp_${{N}}_{kappa_D}.egv_${{iNu}}_${{potential}}_Nmax${{Nmax}}.${{freq}}_IT_kmin{kappa_em}${{suf}}"""