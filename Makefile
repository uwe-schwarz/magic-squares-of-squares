.PHONY: test paper clean

test:
	cd research/prime-support && python3 -m unittest discover -v
	cd research/independent-2026-audit && ./run-tests.sh
	cd research/coupled-p2qr-scan && python3 -m unittest discover -v

paper:
	mkdir -p paper/build
	tectonic paper/prime-support-restrictions.tex --outdir paper/build
	cp paper/build/prime-support-restrictions.pdf paper/prime-support-restrictions.pdf

clean:
	rm -rf paper/build
