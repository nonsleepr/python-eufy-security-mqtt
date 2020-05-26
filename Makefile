SHELL := /bin/bash
all: src/eufy_security/mqtt/eufy.crt
.PHONY: all

src/eufy_security/mqtt/eufy.crt:
	openssl s_client \
  -showcerts \
  -connect security-mqtt.eufylife.com:8789 2>/dev/null <<< Q | \
    awk '$$0 ~ ".*BEGIN.*" {c=1} c==1 {print} $$0 ~ ".*END.*" {c=0}' >$@
	curl -sL https://ssl-ccp.godaddy.com/repository/gd_bundle-g2.crt >>$@
