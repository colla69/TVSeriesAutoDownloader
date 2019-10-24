# TVSeriesAutoDownloader

<img src="https://spiritualregurgitationsdotcom.files.wordpress.com/2009/02/2aea2-6a00d83451607369e2011278d6d47928a4-pi.jpg?width=55&height=145" align="right">

Great News Everyone! Finally I sat down to automated something I used to do by hand.
I hope you can profit, from it aswell.

### requirements
- GNU/Linux OS
- git
- python 3.6 or higher

### TL;DR;

```
git clone https://github.com/colla69/TVSeriesAutoDownloader
pip install -r requirements.txt
cd TVSeriesAutoDownloader
```
fit the `conf.json` file to your needs
```
python main.py 
```

### how does it work

It takes advantage of online streaming services, from https://www1.swatchseries.to/. <br>
By looping trough the config file, the downloader will search for working streaming links, 
and download them to your computer via `wget` commands.<br>
**Searching for links takes some time, because of https://www.cloudflare.com**
#### working backends
- vidoza.net
- vshare.eu
- onlystream.tv
- vidtodo.com

### conf.json

```
{
	"outpath": "~/PlexContent/tvshows/",
	'watchseries_link': "https://www1.swatchseries.to/",
	"done_command": "~/PlexContent/syncTVShows",
	"series": [
		{
		"name" : "The Big Bang Theory",
		"linkpart": "big_bang_theory",
		"no": [12]
		}
]}
```
- outpath : output path for your data (SeriesName/seriesNumber/EpisodeName.mp4)
- watchseries_link : link to the site, it's permanently moving.. 
- done_command : command to execute after the downloads are complete 
- series : list of series to download
  - name : name of the series (foldername)
  - linkpart : part of the link to the series (e.g. https://www1.swatchseries.to/serie/big_bang_theory) the search on the site doesn't work at the moment.
  - no : series you whish to download (e.g. [1,2,3,4,5] would be series 1 to 5)

### credits
  colla69 (Andrea Colarieti Tosti)
