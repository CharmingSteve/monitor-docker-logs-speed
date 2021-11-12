#/bin/bash
docker logs -f --tail 0 proxy | pv -f  --delay-start 2 -i 60 --line-mode --rate 2>&1 >/dev/null |  stdbuf -oL tr /\\r \ \\n 