# Starter Makefile; verify the QCC target variant for your QNX SDP.
QCC ?= qcc
QCCFLAGS ?= -Vgcc_ntox86_64
BUILD_DIR ?= build

.PHONY: all clean
all: $(BUILD_DIR)/hvac_server $(BUILD_DIR)/hvac_client

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/hvac_server: ipc.c | $(BUILD_DIR)
	$(QCC) $(QCCFLAGS) -o $@ $<

$(BUILD_DIR)/hvac_client: client.c | $(BUILD_DIR)
	$(QCC) $(QCCFLAGS) -o $@ $<

clean:
	rm -rf $(BUILD_DIR)
