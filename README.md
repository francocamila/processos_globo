# Cadastro e Consulta de processos do STF - Globo Brasília.

### Introdução

Um projeto feito em Django.

### Objetivo

O Site de Cadastro e Consulta de processos do STF foi criado pela equipe de tecnologia da Globo Brasília para automatizar o processo de pesquisa, atualização e cadastro de processos do STF os quais necessita-se acompanhar frequentemente.

### Como rodar e como funciona

Para **visualizar e testar** o site, bem como suas funcionalidades, insira o seguinte comando no terminal:

```sh
docker-compose up --build -d
```

Se já está "buildado":

```sh
docker-compose up -d
```

O site estará disponível em:

http://localhost:8000

Uma tela de login irá aparecer, então deve-se criar um super usuário, ou usuário administrador. Para isso, os seguintes comandos devem ser feitos:

```sh
docker-compose exec web bash
```

Então, você estará no bash do container web. Use os comandos do django para criar um superusuário:

```sh
python manage.py createsuperuser
```

Após criar o usuário administrador, saia do bash com CTRL+D. Acesse a página de admin do Django com:

http://localhost:8000/admin

Crie novos usuários.

Após isso, você pode acessar a página de cadastro e listagem de processos após realizar o login. 

Ao cadastrar um processo que deseja acompanhar, insira um e-mail para receber atualizações do processo. Além disso, na página de listagem de processos, você pode ver as últimas atualizações de cada processo cadastrado. Nessa mesma página, os processos que não se deseja mais acompanhar podem ser excluídos.

### Debug

Para ver o que está acontecendo:

```sh
docker-compose logs
```

#### Task 
A atualização de processos ocorre a cada uma hora. A configuração de crontab pode ser modificada em "settings.py". Para mais informações, veja a [documentação do **Celery**](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html).

Para testar a task:

```sh
docker-compose exec web bash
```
No bash do container:

```sh
python manage.py shell
```

```sh
>> from consulta_a_processos.tasks import hello
```

```sh
>> hello()
```
