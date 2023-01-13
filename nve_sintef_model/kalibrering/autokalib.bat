@echo off

:: Denne batch-fil kjører automatisk kalibering i emps-mappen.

:: Bytter tidsavsnitt
python autokalib_funksjoner.py bytt_tsnitt %1
saminn < rutine_bytt_tsnitt_saminn.txt
del rutine_bytt_tsnitt_saminn.txt
stfil < rutine_bytt_tsnitt_stfil.txt
del rutine_bytt_tsnitt_stfil.txt

:: Kjører autokalibrering (stfil kalib med AUTKAL.CSV som input)
python autokalib_funksjoner.py autokalib run
stfil < stfil_script_autkal.txt
del stfil_script_autkal.txt

:: Henter kalibreringsfaktorer til excel
python autokalib_funksjoner.py autokalib hent
stfil < stfil_script_se_kalibfaktorer.txt > kalibreringsfaktorer.txt
del stfil_script_se_kalibfaktorer.txt
python autokalib_funksjoner.py autokalib excel
