# Tower Server
Start tower server to relay tasks from client to host.

```
docker build -t tower_server .
docker run -p 7777:7777 tower_server 7777
```
Change `--net`/`--ip`/exposed port if you want.
