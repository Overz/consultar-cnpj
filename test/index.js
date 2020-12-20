var axios = require('axios');
var data = JSON.stringify({ cnpj: '03709814000198' });

var config = {
  method: 'post',
  url: 'http://localhost:3000',
  headers: {
    'Content-Type': 'application/json',
  },
  data: data,
};

axios(config)
  .then(function (response) {
    console.log(response.data);
  })
  .catch(function (error) {
    console.log(error);
  });
