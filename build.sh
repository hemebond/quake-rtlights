#!/bin/bash

MODS=( ad copper dopa dpmod hipnotic id1 jam9 quake15 quoth rogue rrp rubicon rubicon2 )

if [ -z "$2" ]
	then
		# no suffix/version provided
		suffix=""
else
	suffix="-$2"
fi

PK3="rtlights-$1$suffix.pk3"
ARK="$PK3.7z"

if [ -d "$1" ]; then
	(cd "$1" && zip --compression-method store $PK3 maps/*.rtlights)
	git ls-tree --name-only -r HEAD | grep cubemaps/ | zip --compression-method store $1/$PK3 -@
	(cd "$1" && 7z a -t7z -m0=lzma -mx=9 -mfb=64 -md=32m -ms=on $ARK $PK3)
	#rm "$1/$PK3"
fi
