#beamer plot slides

Put PDFs into a basic beamer presentation with (some) ease

PRs/edits are welcome.

Robin Aggleton

##Configure it

Configuration is done via a JSON file, e.g. `configuration.json`.
There is info for the title slide, and then a dict for each slide.
Each slide has various fields, including `plots`, which is a list of `[filename, title]` pairs.
The title is optional.

##Run it

```
./make_slides.py <your configuration JSON>
```

For help, do

```
./make_slides.py -h
```
