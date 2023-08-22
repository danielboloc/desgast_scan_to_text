# extract random examples
pdftk ../../data/TWOR_PHD_1_4.pdf cat 2 12 176 268 407 output page_2_random_examples.pdf
pdftk page_2_random_examples.pdf burst

# works
rm doc_data.txt
for i in /home/daniel_master/workspace/softprojects/desgast_scan_to_text/tests/page_2/pg_*.pdf; do
	pdfimages -j "$i" `basename "$i" .pdf`
	rm pg_*-001.jpg
done

# The .jsons are from "https://portal.vision.cognitive.azure.com/demo/extract-text-from-images", by uploading the images and getting the JSON