# back-end-challenge-pdv
API com a função de resolver o seguinte problema:<br />
Você está no churrasco com o pessoal e acabou a cerveja? A galera já bebeu umas latinhas e ninguém pode dirigir, certo? Imagina você ter algum modo de pedir umas cervejas online e algum PDV te entregar geladinha e em até 1 hora (ah, e com preço de mercado, claro).

## Requisitos
Python 3.6<br />
MongoDB v4.0<br />

## Instalação
git clone https://github.com/anderson-matheus/back-end-challenge-pdv.git<br />
cd back-end-challenge-pdv<br />
cp config.json.example config.json<br />
No arquivo config.json deve ser colocado as configurações do seu banco de dados MongoDB<br />
virtualenv venv<br />
source venv/bin/activate<br />
pip3 install -r requirements.txt<br />
python3 run.py<br />

## Testes
pytest tests.py

## Documentação da API
Link com os endpoits da API: https://web.postman.co/collections/1164449-813d512a-132f-4fae-b80c-a380fa188ff3<br />
<a href="https://web.postman.co/collections/1164449-813d512a-132f-4fae-b80c-a380fa188ff3" target="_blank">Documentação</a>
