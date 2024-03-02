To reproduce the lab run:
```bash
docker compose up -d
```

All of the results will be stored in the logs folder.

Because the datetime field wasn't in ISO format and mongo native query language doesn't suuport
other formats, the last task with adding last n values to capped collection didn't work, but the
query is there.