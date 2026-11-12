# Family Vacations

Trip guides, published with GitHub Pages: https://tulip-controller.github.io/vacations/

- [Okinawa & Ishigaki 2026](okinawa-2026/)

## Put a trip on a Google map

`tools/export_mymaps.py` turns a guide page into CSV files for [Google My Maps](https://www.google.com/mymaps):

```bash
python tools/export_mymaps.py okinawa-2026/index.html
```

Files for the Okinawa trip are already in [okinawa-2026/maps](okinawa-2026/maps). To import one: create a new map, click **Import**, choose the CSV, pick **Search** as the location column and **Name** as the title, then style the layer by **Category**. The map then shows up in the Google Maps app under **Saved → Maps**.
