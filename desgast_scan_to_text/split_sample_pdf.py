import subprocess
import os

def split_sample_pdf_in_dirs(n_pages):
    """Split PDF into 7 pages per sample and create a dir for each sample"""

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.realpath(os.path.join(dir_path, "../data/first_samples"))

    #pdf = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/first_samples/first_samples.pdf"
    pdf = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/samples_39_to_80/samples_39_to_80.pdf"

    #out_path = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/first_samples/"
    out_path = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/samples_39_to_80/"

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

#split_sample_pdf_in_dirs(309)
split_sample_pdf_in_dirs(280)


def connect_to_azure():
    """BIG FAIL: works really bad
    Dit it manually for the pages
    """
    import json
    import requests

    AZURE_ENDPOINT = "https://desgast-scan-to-text.cognitiveservices.azure.com/"
    AZURE_API_KEY1 = "d29eadcdbc1e459ca47fed82d450e656"
    AZURE_API_KEY2 = "243d4104aaa34d8a9d7a9ca6b4f339ef"
    AZURE_REGION   = "eastus"

    # Add your Computer Vision subscription key and endpoint to your environment variables.
    subscription_key = AZURE_API_KEY1
    endpoint = AZURE_ENDPOINT + "/computervision/imageanalysis:analyze?api-version=2023-02-01-preview"

    path_to_file = "/home/daniel_master/workspace/softprojects/desgast_scan_to_text/data/first_samples/sample_1/pg_0003-000.jpg"

    # Read file
    with open(path_to_file, 'rb') as f:
        data = f.read()

    # Request headers.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters. All of them are optional.
    params = {
        'detectOrientation': 'true',
    }
    data = {'url': path_to_file}
    response = requests.post(endpoint, params=params, data=data)

    data_json = response.json()

    analysis = response.json()

    print(analysis)

    # worked with online images (but i couldn't get it to work with local)
    # https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/REST/python-print-text.md
    # 