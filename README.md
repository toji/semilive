SemiLive
=======================
SemiLive is a really simple Sublime Text 3 plugin that advances through a series
of text injection steps, making it appear as if you are typing as you go and
then highlighting the injected text afterwards. Useful for doing "Live Code"
walkthroughs where you want to build up a code file as you narrate and have it
be runnable, but didn't have time to practice and are panicking on a Friday
night about how you could possible memorize all of that code in time. *ahem*

The plugin has the nice properties of visually "typing" the injected strings so
that observers are visually drawn to the motion to more easily follow along. It
also highlights the typed text after each step to help it stand out.

I used it for the demo coding section of my [2017 Google I/O talk](https://youtu.be/jT2mR9WzJ7Y?t=18m16s)

Is this cheating?
-----------------
Yes, Absolutely. But that probably doesn't matter. If you're "live coding" to
show off your typing skills then you shouldn't use this. But chances are that
your audience is more interested in hearing you explain what's happening at
each step than watching you hammer away at a keyboard.

How to use
----------
Drop semilive.py and semilive.sublime-settings into your Sublime Text 3
"Packages/User" directory. (Find it by going to the
"Preferences->Browse Packages" menu item). Then you can run the plugin commands
from the console or (more usefully) bind them to shortcut keys.

 - `semilive_next`: Play the next step in the script
 - `semilive_reset`: Reset the step counter to 0

The script is defined in the `semilive.sublime-settings` file. A `script` array
defines a series of JSON objects that use the following keys:

 - `after`: A string to search for which the `insert` text will be inserted after
 - `replace`: A string to search for which will be replaced by the `insert` text
 - `insert`: A string or list of strings to be inserted after the `after` string or which will replace the `replace` string
 - `instant`: If true will not simulate typing character by character
 - `highlight`: If false will not highlight the `insert` strings after insertion

For examples see the default `semilive.sublime-settings`
