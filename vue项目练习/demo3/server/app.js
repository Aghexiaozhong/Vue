var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');   //cookie的中间件
var logger = require('morgan');  //对日志进行输出
var ejs = require('ejs');
var indexRouter = require('./routes/index');  //渲染首页
var usersRouter = require('./routes/users');  //渲染用户的
var goodsRouter = require('./routes/goods');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.engine('.html',ejs.__express);
app.set('view engine', 'html');  //设置 引擎

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

//在进入路由之前，先全局拦截，查看用户是否处于登录状态
app.use(function (req,res,next) {
    if(req.cookies.userId){
      next();
    }else{
      //设置url白名单  ，比如用户的登录和登出  而访问商品列表的url 是 类似http://localhost:8080/goods?page=1&pageSize=8&sort=1&priceLevel=all
      //不止是/goods  所以URL中存在/goods/list (访问商品列表的URL)即可
      if(req.originalUrl == '/users/login' || req.originalUrl == '/users/logout' || req.path == '/goods/list'){
        next();
      }else{
        res.json({
          status:'1001',
          msg:'当前未登录',
          result:''
        });
      }
    }
});

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/goods',goodsRouter);
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
