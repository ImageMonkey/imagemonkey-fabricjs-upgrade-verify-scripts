# README

This is a collection of scripts that can be used to regression-test fabric.js in the [imagemonkey-core](https://github.com/bbernhard/imagemonkey-core) project.

## Why

Currently ImageMonkey has over 100k annotations in it's dataset - almost all of them created via the webinterface and fabric.js. Although fabric.js has a pretty good test coverage (with over 1000 tests, see [here](http://fabricjs.com/test/) for details) upgrading fabric.js in the imagemonkey-core repository is always a bit risky, we could potentially damage a lot of data when there's a bug in the implementation. Therefore, this set of validation scripts were created which verify whether ImageMonkey behaves the same after the fabric.js dependency upgrade. 

## How does it work

* Create a new git branch in the imagemonkey-core repository (e.g: `fabricjs-upgrade`) which contains the fabric.js dependency upgrade
* Create two folders in the `/tmp` directory. e.g: `/tmp/before-fabricjs-upgrade` and `/tmp/after-fabricjs-upgrade`

Now, start the ImageMonkey services in the `develop`/`master` branch and run the following script: 

```go run snapshot_annotations.go -num=<num> -output-folder="/tmp/before-fabricjs-upgrade" --snapshot-script=snapshot.js -seed=<seed>```

`<num> contains the number of annotations that you would like to analyse
`<seed> needs to be replaced with a random integer value.

e.g:

```go run snapshot_annotations.go -num=1000 -output-folder="/tmp/before-fabricjs-upgrade" --snapshot-script=snapshot.js -seed=12121281281```

The command above now opens 1000 random annotations from the dataset in the unified mode and snapshots the annotations to the `/tmp/before-fabricjs-upgrade` folder.


Next, switch to the `fabricjs-upgrade` feature branch with git (i.e: `git checkout fabricjs-upgrade`) and **restart all the ImageMonkey services.**

Now, run the same script as above with **the same number of annotations and the same seed.**

e.g:

```go run snapshot_annotations.go -num=1000 -output-folder="/tmp/after-fabricjs-upgrade" --snapshot-script=snapshot.js -seed=12121281281```

ImageMonkey now uses the upgraded fabric.js from the feature branch to render the annotations in the unified mode and this script snapshots each of those
annotations to the `/tmp/after-fabricjs-upgrade` folder. 

So we now have screenshots from before the fabric.js upgrade and afterwards. Let's visually compare the images. 

Therefore, run: 

```python3 compare_screenshots.py --folder1="/tmp/before-fabricjs-upgrade" --folder2="/tmp/after-fabricjs-upgrade" --threshold=1.0```

This visually compares the screenshot from before upgrading fabric.js to the one after upgrading fabric.js. With the `--threshold` parameter it's possible to
specify how similar the images need to be (if you want to strive for identical (i.e all pixels are matching) images, use `1.0`). 

If all annotations match, the new fabric.js release is likely to regression free (at least for the ImageMonkey usecase ;-))

