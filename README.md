# VariantAlert 

[VariantAlert](http://variant-alert.crs4.it/) is a free service that annotates variants provided by the user using multiple variant annotation databases.

To keep users informed about updates, the annotation is repeated daily and if a change is detected the user is notified by email.

For more details, please see [About](http://variant-alert.crs4.it/about) section.

VariantAlert is developed and is hosted by [CRS4](http://www.crs4.it/), Italy.
## Requirements

### Docker
- [docker-engine](https://docs.docker.com/engine/installation/) 
- [docker-compose](https://docs.docker.com/compose/install/) 

See [docker-compose docs](https://docs.docker.com/compose/reference/overview/)

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
    EMAIL_USER=your@yourserver.com \
    EMAIL_PASSWORD=your-email-account-password \
    EMAIL_PORT=your-server-port \
    HOST=0.0.0.0 \
  start-local
```

4 - Point your browser to: 
`http://0.0.0.0:8000
 
 
#### Other commands
 
Bring down the VariantAlert app
```bash
make stop
```

From the second execution
```bash
make start-local
```

Remove VariantAlert app from your machine
```bash
make clean
```

Print the help message
```bash
make help
```

## How to cite VariantAlert
To reference VariantAlert in your work, please cite the "http://variant-alert.crs4.it" URL.
