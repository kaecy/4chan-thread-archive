# 4Chan Archive

Command line utility for making archives of 4chan threads.

# About
Quick and easy way to save 4chan threads with a tiny script.

This package uses the official [4chan API](https://github.com/4chan/4chan-APi). You might want to check it if you're writing an archiving package like this.

# Install, Use and Uninstall
Requirements (you don't need these versions, should work with any):
- python-3.13
- requests (gets installed automatically)

## Install
Did you know you can install git-repos as python packages?

Run this command: `pip install git+https://github.com/kaecy/4chan-thread-archive`

Using that command installs the fourchan_archive package and it contains the `4chan_thread_archive` command.

You can use it like this:
```terminal
CMD> 4chan_thread_archive https://boards.4chan.org/g/thread/104564486
```

Output of this command might be:
```output
104564486
│   archive.md
│   metadata.json
│
└──media
    1740775509915344.gif
    1740776973424429.png
    1740779765219202.png
    1740788583272380.jpg
    1740792220753495.gif
    1740794798183558.png
    1740816676848213.jpg
    1740837503345019.png
    1740837671794722.png
    1740838322231522.png
    1740863855376765.jpg
    1740877276036268.jpg
    1740884470385716.png
    1740908610620831.png
    1740912800623499.png
    1740916344435318.gif
    1740928552625726.jpg
    1740928729919557.png
    1740932932750590.png
    1740933228506375.jpg
    1740933539909722.jpg
    1740934180910865.png
    1740934242739373.png
    1740947814907885.png
    1740952209324021.gif
    1740954854373117.png
    1740956734000179.png
    1740957209024984.png
    1740968114783416.jpg
    1740975565606174.jpg
    1740989839279731.jpg
    1740996561455942.png
```
That's your archive.

Keep the `metadata.json` file. You can use it to format the document using different transformation methods which this project can't (yet). There may be other projects that can. Maybe, you can help.

## Uninstall
To uninstall: `pip uninstall fourchan_archive`.

You can uninstall **requests** too, if you aren't going to use it.
