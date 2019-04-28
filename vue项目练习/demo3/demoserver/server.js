

//创建一个服务器
let http = require('http');
let url = require('url');
let util = require('util');
//通过fs文件系统来读取
let fs = require('fs');

let server = http.createServer((req,res)=>{
  //状态吗
  //res.statusCode = 200;
  //res.setHeader('Content-type','text/plain; charset=utf-8');
  var pathname = url.parse(req.url).pathname;
  fs.readFile(pathname.substring(1),function (err,data) {
    if(err){
      res.writeHead(404,{
        "Content-Type":'text/html'
      });
    }else{
      res.writeHead(200,{
        "Content-Type":'text/html'
      });
      res.write(data.toString());
    }
    res.end();  // 输出响应结果
  });


});
//nodejs 默认端口是3000
server.listen(3000,'127.0.0.1',()=>{
  //nodejs 不能获取完整的url  只是获取的相对路径
  console.log('服务器已经运行 请打开浏览器，输入http://127.0.0.1:3000来惊醒访问');
});
