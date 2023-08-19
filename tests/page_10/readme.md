# extract random examples
pdftk ../data/TWOR_PHD_1_4.pdf cat 20 31 41 51 61 193 375 464 454 444 434 output page_10_random_examples.pdf
pdftk page_10_random_examples.pdf burst

# for 'convert'
sudo apt install graphicsmagick-imagemagick-compat  # version 1.4+really1.3.38-1ubuntu0.1, or
sudo apt install imagemagick-6.q16                  # version 8:6.9.11.60+dfsg-1.3ubuntu0.22.04.3
sudo apt install imagemagick-6.q16hdri              # version 8:6.9.11.60+dfsg-1.3ubuntu0.22.04.3

# convert to images (does not work good)
for i in /home/daniel_master/workspace/softprojects/desgast_scan_to_text/tests/page_10/*.pdf; do
	convert -colorspace RGB -interlace none -quality 100 "$i" /home/daniel_master/workspace/softprojects/desgast_scan_to_text/tests/page_10/`basename "$i" .pdf`.jpg
done

# works
for i in /home/daniel_master/workspace/softprojects/desgast_scan_to_text/tests/page_10/pg_*.pdf; do
	pdfimages -j "$i" `basename "$i" .pdf`
	rm pg_*-001.jpg
done
