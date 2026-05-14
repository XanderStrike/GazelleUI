# api

set/get api key in settings ui, then call with bearer auth.

## artist search

```bash
curl -s \
  -H "authorization: bearer $GAZELLEUI_API_KEY" \
  "http://localhost:2020/api/v1/artists/search?q=boards%20of%20canada"
```

## queue download

```bash
curl -s -X POST \
  -H "authorization: bearer $GAZELLEUI_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "torrent_id": 123,
    "artist": "Boards of Canada",
    "album": "Music Has the Right to Children",
    "display_title": "1998 / warp",
    "media": "CD",
    "format": "FLAC",
    "encoding": "Lossless"
  }' \
  "http://localhost:2020/api/v1/downloads"
```
