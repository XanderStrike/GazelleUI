# API

set/get api key in settings ui, then call with bearer auth.

## Artist Search

```bash
curl -s \
  -H "authorization: bearer $GAZELLEUI_API_KEY" \
  "http://localhost:2020/api/v1/artists/search?q=boards%20of%20canada"
```

## Queue Download

Only requires the torrent id — the server looks up the rest from its cache (or fetches from the tracker).

```bash
curl -s -X POST \
  -H "authorization: bearer $GAZELLEUI_API_KEY" \
  -H "content-type: application/json" \
  -d '{"torrent_id": 123}' \
  "http://localhost:2020/api/v1/downloads"
```

## List Downloads

```bash
curl -s \
  -H "authorization: bearer $GAZELLEUI_API_KEY" \
  "http://localhost:2020/api/v1/downloads?status=queued&limit=10"
```

Query params:
- `status` — optional, `queued` or `downloaded`
- `limit` — optional, max 500, default 50
