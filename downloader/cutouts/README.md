# Cutout Gathering

Grabbing cutouts from various surveys

**The code currently is in a testing phase**, and at the moment grabs ~140 Best & Heckman galaxies as FITS files from all included surveys.

### Currently included surveys:

| Survey | Band | 
|---|---|
| FIRST | Radio |
| NVSS | Radio|  
| VLASS| Radio| 
| SDSS| Optical| 
| PanSTARRS| Optical| 

### Surveys to include:

| Survey | Band| 
|---|---|
|LoTSS|Radio|
|AKARI|Infrared|
|WISE|Infrared|
|BOSS|Optical|
|GALEX|Ultraviolet|
|3XMMRLQSO|X-Ray|
|RASS|X-Ray|
|FERMI (LAT)|Gamma-Ray|
|HESS|Gamma-Ray|

---

### How to run

From the shell:

`mkdir out
python3 main.py`

This will fill `out` with the FITS files

**FITS Processing to JPEG**

`python3 process_fits.py`

This takes whatever supported FITS files are in `out` and processes them into `.jpg`'s.
_All included surveys (see above) are supported_

### Installation Notes

You'll need to install <a target=_blank href="https://montage-wrapper.readthedocs.io/en/v0.9.5/#installation">Montage</a>, among other standard fair, which can be a littly tricky. Here's the Coles Notes:

 * Download `http://montage.ipac.caltech.edu/download/Montage_v5.0.tar.gz` from <a target=_blank href="http://montage.ipac.caltech.edu/docs/download2.html">`http://montage.ipac.caltech.edu/docs/download2.html`</a>.
 * `tar xvzf Montage_v5.0.tar.gz`
 * Got into the `Montage_v5.0` and type `make` to build.
 * Move the `Montage_v5.0` to `~/.montage/Montage_v5.0`, say, and add `~/.montage/Montage_v5.0/bin` to `$PATH`.
 * To test, run `mAdd` and you should see something like,<br>```[struct stat="ERROR", msg="Usage: mAdd [-d level] [-p imgdir] [-n(o-areas)] [-a mean|median|count] [-e(xact-size)] [-s statusfile] images.tbl template.hdr out.fits"]```<br>indicating it is installed correctly.