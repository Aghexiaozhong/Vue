
var http = require('http');

let util = require('util');

http.get('http://www.imooc.com/u/card',(res)=>{
  let data = '';
  //获取数据一次一次取的，通过监听使得数据不断的累加
  res.on('data',(chunk)=>{    //监听数据
    data += chunk;
  });
  res.on('end',function () {


    data = data.slice(14,-1);

    let result = JSON.parse(data);

    console.log(util.inspect(result));
  });     //监听最后的响应
});
