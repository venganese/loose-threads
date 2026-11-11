# Loose Threads

A made-up fashion store built to show three website tricks that don't look AI-generated. Nothing here is for sale.

| Page | Trick |
|---|---|
| **Hello** (`hello.html`) | *Dress like what's trending*: today's #1 song and movie (Apple's charts for the visitor's country) and trending book (Open Library), each paired with an outfit from the store. No API key, no server. |
| **Shop** (`index.html`) | Every product is 3,400 particles. Scroll and they fall apart and rebuild into the next piece. |
| **About** (`about.html`) | ~~Read~~ **Ask** About Us: type a question and a small embedding model, running in the visitor's browser, picks the right answer card. |

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000/hello.html
```

## What's in here

```
index.html  hello.html  about.html     the published pages (index and hello are generated, see build/)
models/     all-MiniLM-L6-v2, 8-bit ONNX            (served from this site, not Hugging Face)
vendor/     transformers.js 3.8.1 + ONNX Runtime    (served from this site, not a CDN)
download_model.sh                        re-downloads models/ and vendor/ if you ever need fresh copies
build/
  build.py                  → regenerates index.html and hello.html
  template.html             Shop page source
  trending_template.html    Hello page source
  to_4shade.py              product photo → 512×512, 4-shade particle target
  src/  out/                product photos and their 4-shade targets
```

`about.html` is edited directly. To change the Shop or Hello page, edit the template in `build/`, then:

```bash
pip install pillow numpy
python3 build/to_4shade.py build/src build/out   # only if product photos changed
python3 build/build.py
```

## How it works

- **Particles:** each photo becomes a 4-shade, 512×512 image. 3,400 points are sampled from it, weighted by darkness, then ordered along a Hilbert curve so each particle travels between nearby spots in consecutive shapes. Scroll position blends shape A → scatter → shape B. No neural network.
- **Ask box:** each answer card's example questions are embedded once when the page loads. A question is embedded and matched to the closest card: a score of 0.38 or more is an answer, 0.33–0.38 is tagged "Best guess", and anything lower gets "No card for that yet". If the model can't load, the page falls back to keyword matching.
- **Trending:** genre and subject words choose a mood (loud, soft, stealth, dark, earthy, bright or easy), and each mood chooses one of three outfits, rotating daily. The visitor's country comes from their time zone (then browser language), with India's charts as the fallback.

## Credits

- Charts: Apple iTunes RSS feeds and [Open Library](https://openlibrary.org) trending, fetched live in the browser.
- Model: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (Apache-2.0), ONNX export by [Xenova](https://huggingface.co/Xenova/all-MiniLM-L6-v2).
- Runtime: [Transformers.js](https://github.com/huggingface/transformers.js) (Apache-2.0) and [ONNX Runtime Web](https://github.com/microsoft/onnxruntime) (MIT).
- Font: [Archivo](https://fonts.google.com/specimen/Archivo) (SIL OFL), via Google Fonts.
- Product photos belong to their respective owners and are used here only for a non-commercial demo.
