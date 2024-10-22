# ZTA Lightning

**ZTA Lightning** is an automated compliance framework designed to audit your network devices on Zero Trust Architecture (ZTA) principles. 
It interacts with your network appliance responsible for Authentication, Authorization, and Accounting (AAA) as well as Network Management Systems (NMS) to gather configuration and security data. 
The tool outputs a detailed Excel report of the compliance audit results.

## Features
- **ZTA Compliance Check**: Evaluates your network devices against specific Zero Trust principles.
  - In the current version, these include:
    - Logging and Monitoring
    - Authentication and Access Control
    - Network Segementation
    - Least Privilege
- **Excel Report Generation**: Provides a summary of the compliance results in an Excel file.
- **Network Appliance Integration**: Works with network appliances that have AAA and NMS functionalities.
- **JWT Authentication**: Supports secure authentication via JSON Web Tokens (JWT).
- **HTTPS Communication**: Ensures encrypted communication with the network appliance.

## Prerequisites
Before using ZTA Lightning, ensure you have the following:
- **URL** of your network appliance (responsible for AAA and NMS).
- **Credentials** to authenticate with the appliance.
- **HTTPS** enabled on the appliance for secure communication.
- **JWT** enabled for authentication.

## How to Install

Clone the repository to your local machine:
```
git clone https://github.com/jschmidt777/zta-lightning.git
```
Navigate to the project directory:
```
cd zta-lightning
```
Install the required dependencies (using pip or another package manager):
```
pip install -r requirements.txt
```

## How to Use

Ensure to provide an `.env` file with the following configuration options set before running the tool:
- JWT_SECRET_KEY (string: used for the simulated appliance to create JWTs)
- VERIFY_SSL (boolean: tells the tool to verify SSL for HTTPS 2.0; not required with running against the simulated appliance)
- USE_HTTPS (boolean: enables HTTPS on the simulated appliance)

1. Ensure that your network appliance has both HTTPS and JWT authentication enabled.

2. Run the tool from the command line. You will be prompted to provide the URL of the appliance and the necessary authentication credentials.

3. The tool will gather data from the appliance regarding network devices and their configurations.

4. ZTA Lightning will evaluate this data against Zero Trust principles and generate an Excel (.xlsx) report detailing the compliance results.

```
python -m app.zta_lightning.py
```

5. Once the tool has finished running, the report will be saved in the same directory where the tool was executed.

## Example Usage
```
$ python -m app.zta_lightning.py
Enter the AAA/NMS appliance URL: https://appliance.example.com
Enter your username: admin
Enter your password: ********
```
After the tool completes its checks, the output file will be saved with the current date of when the report was created.
