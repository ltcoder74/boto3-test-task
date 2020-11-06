# Fetrewrds DevOps Test Task

## Setup
- Install requirements
```
pip install -r requirements.txt
```
- Add a user with programatic access in IAM and attach permissions for AmazonEC2FullAccess, IAMFullAccess and AmazonSSMFullAccess
- Configure aws locally
```
aws configure
```
- Populate config.yaml according to your requirements
- Populate settings.py
- Generate keypair
```
python generate_keypair.py
```
- Run script
```
python main.py
```
