import axios from 'axios';
import { cnpj } from 'cpf-cnpj-validator';

const request = () => axios.create({ baseURL: 'http://localhost:3000' });

request()
  .post('/', { cnpj: '07742830000133' || cnpj.generate(false) })
  .then((r) => console.log(r.data))
  .catch((e) => console.log(e));
