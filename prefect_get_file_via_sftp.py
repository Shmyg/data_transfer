from prefect import flow, task
from get_ftp_file import download_file

@task
def download_file_task():
    result = download_file()
    return result

@flow(name="Nightly FTP Download")
def ftp_flow():
    download_file_task()

if __name__ == "__main__":
    ftp_flow()