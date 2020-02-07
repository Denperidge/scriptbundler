# Scriptbundler

An experimental tool to bundle multiple scripts into one single script file.

## Why put multiple scripts into one?

With a large scale script project, it's a lot easier during development to split it up into multiple files. Then you can easily insert those into large and/or packaged applications. But when your application *is* the script, requiring the end user to download a whole directory full of them would be very non-user-friendly, while developing in one gigantic script could make development a lot harder.

## Usage example

Put any amount of shell/batch/powershell scripts in the input directory, run `python build.py` , specify the order the scripts should be run in, and done!

![A very small demo gif for scriptbundler](/readme/demo.gif)

## Important note

Bundling multiple scripts of the same type (e.g. .sh/.bat/.ps1) should normally give no issue. However, if you wish to combine (for example) a .sh and a .bat into one .sh script, the bundler will perform some basic translation (in this example prepending cmd.exe before the .bat commands). This is a proof-of-concept feature and primitive at best. For simple uses it should work fine, but do not expect variables etc. to pass flawlessly.

The bundling will work out of the box for any OS, but translating (f.e. combining a ps script and a shell script) is by default configured for a Windows environment. But, with some modification to the templates in convert.py, it shouldn't take too long to let the translator fit your favourite OS.
