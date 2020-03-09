<table align="center"><tr><td align="center" width="9999">

<img src="https://pa1.narvii.com/6899/8138ae9d1101b4468e6ab9502d5b00ba5701fa9er1-600-400_00.gif" align="center" width="200" alt="Project icon">

# Kessel API

>![GraphQl Badge](https://badgen.net/badge/icon/graphql/pink?icon=graphql&label)
[![Docs Link](https://badgen.net/badge/docs/github_wiki?icon=github)](https://github.com/brunolcarli/Kessel/wiki)
![Version badge](https://img.shields.io/badge/version-0.0.9-green.svg)


API Backend for unamed discord game!

</td></tr></table>

# Rodando

![Linux Badge](https://img.shields.io/badge/OS-Linux-black.svg)
![Apple badge](https://badgen.net/badge/OS/OSX/:color?icon=apple)

## - Local

Para rodar a plataforma localmente, primeiramente é necessário inicializar um novo ambiente virtual (virtualenv) e instalar as depenências:

```
$ make install_local
```

Crie um arquivo contendo as variáveis de ambiente conforme o `template` disponível em [kessel/environment/](https://github.com/brunolcarli/kessel/blob/develop/kessel/environment/template) contendo as variáveis para seu ambiente de execução (por exemplo: *my_env_file*)

```
$ source my_env_file
```

Iniciar a plataforma com o comando:

```
$ make run_local
```


O serviço estará disponível em `localhost:5666/graphql`

<hr />

<table align="center"><tr><td align="center" width="9999">


<img src="https://vignette.wikia.nocookie.net/es.starwars/images/1/11/Summa-Verminoth.jpg/revision/latest?cb=20190227235016" align="center" width="300" alt="Project icon">

</td></tr>

</table>

![docker badge](https://badgen.net/badge/icon/docker?icon=docker&label)

## - Docker

Crie um arquivo `kessel.env` em  `kessel/environment/kessel.env` e adicone as variáveis de ambiente:

Insira e preencha neste arquivo as seguintes variáveis de ambiente:

```
DJANGO_SECRET_KEY=<your_secret_key>
DJANGO_SETTINGS_MODULE=kessel.settings.production

MYSQL_ROOT_PASSWORD=<your_database_root_password>
MYSQL_USER=<your_database_user>
MYSQL_DATABASE=<your_database_name>
MYSQL_PASSWORD=<your_database_password>
MYSQL_HOST=kessel_db
```

Instale o docker compose:

```
$ pip install docker-compose
```

Suba os containers com:

```
$ make docker
```
