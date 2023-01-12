# cryogenesis-rando

Randomizer for Super Metroid romhack "Cryogenesis" by Onnyks

Python 3

Presemnted as-is, and I don't intend to do many updates

1. Download this repository
2. Put your cryogenesis 1.0 rom in the roms folder with the name Cryogenesis.sfc
3. Run Main.py to gen a seed

Built from the engine at https://github.com/SubversionRando/SubversionRando
This uses assumed fill to gen the seeds
Many of the files here are no longer needed, as I ripped the guts out of it and left some things lying around

Logic:
Some tricks may be required to beat the seed, and softlocks are possible if you enter certain areas without a way to escape. Items will only logically be placed in areas that you can enter AND escape. This tends to put morph at "BT", but a few other configurations are possible. If you enter the Meteorite warehouse without Meteorite, you will be unable to escape. Meteorite will not be placed there.

I added Speed Booster and Plasma into the game and logic, as the data was leftover in the rom even though those items do not appear in Cryogenesis. Meteorite blocks can be broken by meteorite OR speed!
