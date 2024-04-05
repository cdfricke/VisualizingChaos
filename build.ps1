# Programmer: Connor Fricke (fricke.59@osu.edu)
# File: build.ps1
# PWSH Script to act essentially as a Windows version of a Makefile.
# For compiling and linking the VisualizingChaos projects C++ dependencies,
# in addition to outputting useful info to the console for the user.
# To Run:
# PS > .\build.ps1

# get the working directory path
$scriptPath = $MyInvocation.MyCommand.path
$dir = Split-Path -Parent $scriptPath
Write-Output "Current Directory: $dir"

# TEST GNUPLOT FUNCTIONALITY
#Write-Output "Testing Gnuplot Connection... (opening window)"
#gnuplot --persist 'misc\\test.plt'
#Write-Output "Gnuplot Testing Stage Complete."

# compile and link dependencies of C++ programs
# this includes diffeq_pendulum.cpp, diffeq_routines.cpp, GnuplotPipe.cpp
Write-Output "Compiling and Linking C++ Program Dependencies..."
# compile diffeq_pendulum
g++ -c -g -Wall -O1 -o $dir\misc\diffeq_pendulum.o $dir\dependencies\diffeq_pendulum.cpp 
# compile diffeq_routines
g++ -c -g -Wall -O1 -o $dir\misc\diffeq_routines.o $dir\dependencies\diffeq_routines.cpp
# compile GnuplotPipe
g++ -c -g -Wall -O1 -o $dir\misc\GnuplotPipe.o $dir\dependencies\GnuplotPipe.cpp
# link .o files to create an executable
g++ -o diffeq_pendulum.exe $dir\misc\diffeq_pendulum.o $dir\misc\diffeq_routines.o $dir\misc\GnuplotPipe.o
Write-Output "Compiling Stage Complete."

# run C++ program!
$userInput = Read-Host -Prompt "Start C++ Program? Y/N"
if ($userInput -eq "Y")
{
    .\diffeq_pendulum.exe
}
else {
    Write-Host "Process terminated."
}

# install Python modules, dump output to misc\null
Write-Output "Installing Python Modules: PyGame, Matplotlib"
python.exe -m pip install PyGame Matplotlib > $dir\misc\null
Write-Output "Module Install Stage Complete."

# run python script!
$userInput = Read-Host -Prompt "Start Python simulation? Y/N"
while ($userInput -eq "Y") {
    python.exe .\python\pendulum.py
    $userInput = Read-Host -Prompt "Again? Y/N"
}
Write-Output "Process Terminated."

# THANKS!
Write-Output "Thank you! Have a great day! - Connor"




