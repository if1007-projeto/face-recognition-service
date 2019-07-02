# Face Recognition Service

Serviço responsável por ler do Kafka as faces recortadas e assim fazer o reconhecimento caso haja uma face conhecida no base de dados.

## Requisitos

A aplicação foi testada com as ferramentas e versões abaixo.

* Python 3+
  
**Observação**: O `docker-compose.yml` possui alguns parâmetros que só estão presentes no docker-compose versão utilize uma versão acima da 1.18, pois utilizamos algumas configurações

### Bibliotecas

* [Kafka Python client](https://github.com/dpkp/kafka-python)
* [Face Recognition](https://github.com/ageitgey/face_recognition)

## Instalação
Para evitar que as dependências sejam desnecessariamente instaladas globalmente, é recomendável criar uma ambiente virtual. Para isto execute os seguintes comandos:

```bash
virtualenv -p python3 .recognize_env
source .recognize_env/bin/activate
```

Agora execute o comando abaixo para instalar as dependências no ambiente virtual criado:

```bash
pip install --no-cache-dir -r requirements.txt
```

## Como utilizar

O primeiro passo a se fazer é criar um diretório com a base de faces conhecidas. Para este passo a passo vamos criar um diretório com o nome `known_faces`:

```bash
mkdir known_faces
```

**Observação**: É importante que as imagens contenham apenas uma face de uma única pessoa. (Não precisa ter pessoas repetidas na base de dados, apenas uma face por pessoa já é o necessário.)

**Dica**: É interessante que cada imagem de face da base seja nomeada com o nome da pessoa.

### Reconhecimento de uma única face

Para fazer o reconhecimento de apenas uma face desconhecida basta executar o seguinte comando:

```bash
python main.py -k known_faces -i unknown_face.jpg
```

O arquivo `unknown_face.jpg` vai ser a imagem da face ser reconhecida. Se a face der match com algumas das faces da base o programa mostrará como saída o nome do arquivo que deu match (por isso é interessante nomear os arquivos da base com o nome das pessoas).

### Reconhecimendo de um conjunto de faces

Para fazer o reconhecimento de um conjunto de faces primeiro deve criar um diretório para as faces desconhecidas, neste passo a passo vamos criar um diretório com o nome `unknown_faces`:

```bash
mkdir unknown_faces
```

Em seguida basta executar o seguinte comando para fazer o reconhecimento no conjunto de faces:

```bash
python main.py -k known_faces -b unknown_faces
```

A saída do programa vai ser semelhante ao do exemplo anterior, porém cada linha vai representar uma face do conjunto de faces desconhecidas.

### Reconhecimento de faces consumindo de um servidor Kafka

Para reconhecer imagens a partir de um servidor kafka basta editar duas variáveis de ambiente declaradas no `docker-compose.yml`. O primeira variável é `KAFKA_URL` onde você deve atribuir o endereço onde o Kafka está sendo executado. A segunda variável é `KAFKA_TOPIC` onde você deve atribuir o nome do tópico que irá fornercer as faces a serem reconhecidas.

Alterando as variáveis citadas acima, basta executar o seguinte comando para "levantar" um container de reconhecimento:

```bash
docker-compose up
```