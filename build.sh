#!/bin/bash

MODS=( ad copper dopa dpmod hipnotic id1 jam9 quake15 quoth rogue rrp rubicon rubicon2 )

if [ -d "$1" ]; then
	(cd "$1" && zip --compression-method store rtlights_$1.pk3 maps/*.rtlights)
	git ls-tree --name-only -r HEAD | grep cubemaps/ | zip --compression-method store $1/rtlights_$1.pk3 -@
fi
