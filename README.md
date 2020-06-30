# VariantAlert 


## Requirements

### Docker
- [docker-engine](https://docs.docker.com/engine/installation/) 
- [docker-compose](https://docs.docker.com/compose/install/) 

See [docker-compose docs](https://docs.docker.com/compose/reference/overview/)

### Self signed certificate (only for localhost)
- [openssl](https://www.openssl.org)

See [Certificates for localhost](https://letsencrypt.org/docs/certificates-for-localhost/)

## Quickstart

The first execution could require several minutes, from the second one will be faster.

1 - Clone the repository:  
```bash
git clone https://github.com/next-crs4/VariantAlert.git
```

2 - Cd into the docker directory:  
```bash
cd VariantAlert
```

3 - Bring up the VariantAlert app
```bash
make EMAIL_HOST=smtp.yourserver.com \
    EMAIL_HOST_USER=your@yourserver.com \
    EMAIL_HOST_PASSWORD=your-email-account-password \
    EMAIL_PORT=your-server-port \
    REAL_URL=https://0.0.0.0 \
  start
```

4 - Point your browser to: 
`https://0.0.0.0`
 
 
#### Other commands
 
Bring down the VariantAlert app
```bash
make stop
```

From the second execution
```bash
make start
```

Remove VariantAlert app from your machine
```bash
make clean
```

Print the help message
```bash
make help
```
