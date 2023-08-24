import subprocess
import os

def split_sample_pdf_in_dirs(n_pages):
    """Split PDF into 7 pages per sample and create a dir for each sample"""

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(dir_path, "../data/first_samples"))

    pdf = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/first_samples/first_samples.pdf"

    out_path = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/first_samples/"

    # for every 7 pages, create 1 folder with the number 'idx'
    for idx, page_num in enumerate(range(7,n_pages,7), 1):
        l = [str(j) for j in range(page_num-6, page_num+1)]

        # had to move in the last command bc gave error when trying to set out dir
        pdftk_cat_burst = f"""
            mkdir {out_path}sample_{idx}/
            pdftk {pdf} cat {' '.join(l)} output {out_path}sample_{idx}/sample_{idx}.pdf
            pdftk {out_path}sample_{idx}/sample_{idx}.pdf burst output {out_path}sample_{idx}/
            rm doc_data.txt
            for i in {out_path}sample_{idx}/pg_*.pdf; do
                pdfimages -j "$i" `basename "$i" .pdf`
                rm pg_*-001.jpg
                mv *.jpg {out_path}sample_{idx}/
            done
        """
        
        run = subprocess.run(pdftk_cat_burst, universal_newlines=True, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if run.stdout is not None:
            print(run.stdout)
        if run.stderr is not None:
            print(run.stderr)
        # print(cp.returncode)

split_sample_pdf_in_dirs(309)