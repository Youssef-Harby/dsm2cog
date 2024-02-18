import boto3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure the S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url="https://opentopography.s3.sdsc.edu",
    aws_access_key_id="raster",
    aws_secret_access_key="SECRET &&&&&&&&&&&&&&&&&& CHANGE",
    region_name="us-west-1",
    use_ssl=True,
    verify=True,
)

bucket_name = "raster"
dsm_data_prefix = "AW3D30/AW3D30_global/"
destination_dir = Path("./dsm_data_egypt")
destination_dir.mkdir(
    parents=True, exist_ok=True
)  # Ensure the destination directory exists
overwrite_files = False

egypt_coordinates = [
    f"N0{lat:02d}E{long:03d}" for lat in range(22, 33) for long in range(25, 36)
]


def list_files_to_download(name):
    files_to_download = []
    file_prefix = f"{dsm_data_prefix}ALPSMLC30_{name}_DSM"
    continuation_token = None
    while True:
        list_objects_params = {
            "Bucket": bucket_name,
            "Prefix": file_prefix,
            **({"ContinuationToken": continuation_token} if continuation_token else {}),
        }
        response = s3_client.list_objects_v2(**list_objects_params)
        if "Contents" in response:
            for obj in response["Contents"]:
                file_key = obj["Key"]
                local_file_path = destination_dir / Path(file_key).name
                if not local_file_path.exists() or overwrite_files:
                    files_to_download.append((file_key, local_file_path))
        if response.get("IsTruncated"):
            continuation_token = response.get("NextContinuationToken")
        else:
            break
    return files_to_download


def download_file(file_info):
    file_key, local_file_path = file_info
    print(f"Downloading {file_key} to {local_file_path}")
    s3_client.download_file(bucket_name, file_key, str(local_file_path))
    return f"Downloaded {file_key}"


# List all files to download
all_files_to_download = []
for name in egypt_coordinates:
    all_files_to_download.extend(list_files_to_download(name))

# Download files in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_file = {
        executor.submit(download_file, file_info): file_info
        for file_info in all_files_to_download
    }
    for future in as_completed(future_to_file):
        file_info = future_to_file[future]
        try:
            result = future.result()
            print(result)
        except Exception as exc:
            print(f"{file_info[1]} generated an exception: {exc}")

print("All downloads completed.")
