# Lost Original

OSINT · 250 points · 7 solves

Flag: `CLUB{Cayambe_2013}` (not case-sensitive)

> This photo was making the rounds, but nobody remembers where it came from. Find the original upload. The flag is CLUB{photographer-username_year}, using the username of whoever uploaded it and the year it was taken.

`lost.png` is a 3520 × 3840 image, about 18 MB, with all metadata stripped. `exiftool` shows no camera, GPS or author fields, so everything has to come from what's in the picture.

The image is cut into a 4×4 grid of tiles that don't line up, and the lettering on the column is mirrored. That's there to stop someone dropping the whole thing into a reverse image search and getting an answer straight away.

## Solving it

1. Mirror the image back with any editor, or `convert -flop`. Then crop out one distinctive tile rather than searching the whole mosaic (hint: "The picture's been flipped and cropped.").

2. The best tile shows a cream fluted column topped with a bust of a woman. The base has a green-and-red decorative panel and the capital is carved with FRATERNITÉ. Around it are red tin roofs, pastel colonial buildings and a tropical sky.

3. Search that tile with several reverse image engines: Google Lens, Bing Visual Search, Yandex and TinEye index different images (hint: "Try more than one search engine."). Even a text search for the details works. The column is the Colonne de la République, a column with a bust of Marianne put up in 1890 for the centenary of the French Revolution. It stands in the Place des Palmistes in Cayenne, French Guiana.

4. Wikimedia Commons has photos of Place des Palmistes and other Cayenne landmarks by the user Cayambe. The file page for the matching photo lists the author and the date it was taken (hint: "Wikimedia Commons keeps the uploader and date on each file's page.").

5. Username plus year: `CLUB{Cayambe_2013}`.

## Easy mistakes

Commons shows both the upload date and the date the photo was taken; the flag uses the year it was taken. Searching the full scrambled image usually returns nothing, so crop first.

Seven teams solved it, the second-highest count of the event.

Photo credit: the original image is by Wikimedia Commons user Cayambe (Cayenne, 2013), used under its Commons licence. `lost.png` is a mirrored and re-tiled version made for the challenge.
