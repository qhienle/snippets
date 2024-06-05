#!/usr/bin/env bash

mkdir Bastille
cd Bastille
mkdir '14 juillet 1789'
touch 'Mort au roi!'
echo 'Guillotine!' > Monarchie
tar -cf 'Vive la France!.tar.gz' Monarchie
rm Monarchie
ls -1
