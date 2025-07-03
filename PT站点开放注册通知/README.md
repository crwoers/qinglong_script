### 1、文件说明
- `pt.json`  PT站点注册链接 
- `signup_send.py` 判断站点是否开启注册并通知开放注册的站点列表

### 2、获取 pt.json 内容
- 在 `iyuu` -> `站点` 页面上 `F12` 打开控制台，在控制台输入以下脚本
- 将 `{domain}` 替换成iyuu部署的地址，如：`http://192.168.100.10:18787`
- 将控制台输出的 `object` 复制到 `pt.json` 文件中
``` javascript
layui.jquery.get('{domain}/admin/site/select?page=1&limit=200').done(function({data}){let list = [];layui.jquery.each(data, function(index, item){ list.push({name: item.nickname + (item.nickname.toUpperCase() == item.site.toUpperCase() ? '' : '（'+ item.site +'）'), href: 'https://' + item.base_url + '/signup.php' });  }); console.log(list);});
```
