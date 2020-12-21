# Consulta de CNPJ

Procura cnpj em [**receita_ws**](https://receitaws.com.br/api) e [**cnpj-rocks**](https://cnpjs.rocks/), ambos sites de consulta. Caso a ReceitaWS atingir o limite de consulta por minuto, o resultado será direcionado para o CNPJ-ROCKS.

Utilizado Python pois não existe a necessidade de instanciar um browser como no puppeteer, para consultar os dados.
