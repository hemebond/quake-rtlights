# rtlights4quake
A collection of rtlights and cubemaps for Quake engines that support real-time lighting files.

## How To
Getting rtlights to work is a fairly straight forward process but requires a few steps.

### Files
The first item you will need is the Quake 1 `.pak` files, they contain the raw data for the game. If you purchase Quake on steam or some other platform you should be able to find the files.

The two paks are called *PAK0.PAK* and *PAK1.PAK*.

In base install mode they should reside in `quake/id1/`

If you so desire you can always keep them in there, or you can move them to a new folder if you plan on altering them (re-vis for example).

The next item you will need is the [Darkplaces ](https://icculus.org/twilight/darkplaces/)engine or another rtlight supporting engine, like [FTE Quake](http://fte.triptohell.info/).

Despite the website being dated, the Darkplaces engine project continues and gets regular updates. Although there are more [recent builds](https://icculus.org/twilight/darkplaces/files/darkplacesengineautobuild.zip), currently the most stable build I have found is one from [April 2018](https://icculus.org/twilight/darkplaces/files/darkplacesengine20180412beta1.zip).

The Darkplaces executable should go in your /quake folder.

The next item required will be the rtlights themselves. Take the `.rtlights` files and place them in the `id1/maps/` directory. The cubemaps should be placed in the `id1/cubemaps/` directory if you wish to use those.


### VISing ID1 Maps
Now that you have all the files you need the next step is to [re-vis your maps](http://vispatch.sourceforge.net/). This process can be fairly annoying, but there are fortunately some easier ways to accomplish it using existing vis data and using that instead of re-compiling maps.

Once you have your maps properly vis'd, launch Darkplaces and turn on real-time lighting, the option can be found in the game menu by going to Options > Customize Lighting > RT World > On . You can also go into the console by hitting tilde (`~`) and typing `r_shadow_realtime_world 1`

That is it, play around with brightness and graphics until you are happy and start playing.

## Graphics Options (DarkPlaces Only)
A few settings you may want to mess with:

For that old school software quake texture feel go to the console (`~`) and type `gl_texturemode gl_nearest`

For some interpreted bumpmap effects on the stock textures go to the console and set `r_shadow_bumpscale_basetexture` to 4 or 5. Be sure type in `r_restart` in the console to enable this change, as it requires the render to reload in order to work.

You can always turn on gloss and coronas as well in the menu, but I personally don’t recommend those effects.

## Editing .rtlights
If you want to play around with the lights themselves type in `r_editlights 1` into the console.

If you are curious about more functions you can always type the start of a command and hit tab, it will show you all the options and a brief explanation of what they do, this is important for `.rtlight` editing, even after doing this for years I still find myself typing `r_editlights_` and hitting the tab key to see all the options.
