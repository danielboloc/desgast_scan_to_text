# extract random examples
pdftk ../../data/TWOR_PHD_1_4.pdf cat 7 17 181 273 412 output page_7_random_examples.pdf
pdftk page_7_random_examples.pdf burst

# works
for i in /home/daniel_master/workspace/softprojects/desgast_scan_to_text/tests/page_7/pg_*.pdf; do
	pdfimages -j "$i" `basename "$i" .pdf`
	rm pg_*-001.jpg
	rm doc_data.txt
done

# The .jsons are from "https://portal.vision.cognitive.azure.com/demo/extract-text-from-images", by uploading the images and getting the JSON