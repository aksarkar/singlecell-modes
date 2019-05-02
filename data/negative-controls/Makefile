CURL = curl -sfL -o $@

all: svensson_chromium_control.h5ad zheng_gemcode_control.h5ad macosko_dropseq_control.h5ad klein_indrops_control.h5ad

svensson_chromium_control.h5ad:
	$(CURL) "https://ndownloader.figshare.com/files/14634410"

zheng_gemcode_control.h5ad:
	$(CURL) "https://ndownloader.figshare.com/files/14634407"

macosko_dropseq_control.h5ad:
	$(CURL) "https://ndownloader.figshare.com/files/14634488"

klein_indrops_control.h5ad:
	$(CURL) "https://ndownloader.figshare.com/files/14634416"
