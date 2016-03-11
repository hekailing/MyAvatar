# MyAvatar
A simple avatar hosting website
## 设计思路
1. 用户登陆与注销
  1. 客户端的每一次登陆，在服务器上生成一个session，作为文件存储在服务器的"/tmp/avatar"目录下。文件命名为sess_xxx，其中xxx为会话ID。会话ID为系统时间+随机数的sha256哈希值。session文件中存储的内容包括：
    * 用户最后一次活动时间
    * 用户名
    * 用户邮箱（由于本站点邮箱固定，因此作为cookie保存，减少数据库操作）
  2. 用户首次登陆时，服务器进行如下操作：
    * 由于用户cookie不存在会话ID，服务器根据系统时间生成会话ID并创建对应的session文件。
    * 将新生成的会话ID写入cookie并发送给客户端
    * 将当前系统时间写入session文件
    * 生成登陆页面
  3. 在登陆页面中进行如下验证并通过后，跳转到欢迎页面；否则显示错误信息并要求重新登陆
    * 用户名和邮箱不得为空
    * 在数据库中查找出用户名对应的密码Hash值和盐，利用用户提供的密码和盐得到Hash值并与数据库中保存的Hash值相比较
  4. 在欢迎页面中需要进行如下操作：
    * 检查cookie中是否存在会话ID，若不存在，将根据系统时间生成会话ID
    * 根据该会话ID寻找对应的session文件，若session文件不存在，则创建新的session文件
    * 将会话ID写入cookie并发送给客户端
    * 检查session文件中的上次登陆时间，查看是否超时，若超时，跳转到登陆页面要求重新登陆，并结束后续操作
    * 检查session文件中的用户信息是否存在且完整，若不完整，则需要进行登陆操作以获取用户信息，具体如下：
      * 如果FieldData中有"login"字段，表明需要服务器处理登陆表单，具体参考用户登陆与注销中的步骤3
      * 如果没有"login"字段，仅仅生成登陆页面
    * 获取用户信息（用户名和邮箱），针对FieldData中的字段情况分别采取下面的操作：
      * 若存在"upload"字段，需要处理头像上传任务，具体参见头像上传
      * 若存在"logout"字段，执行用户登出任务，主要为清除session文件中的用户信息，返回登陆页面
      * 其他情况，只需要刷新欢迎页面
    * 刷新最后访问时间
    * 写入session文件
2. 头像上传
3. 头像下载
4. 创建账户

  一个合法的账户需要满足下列条件：
  * 用户名合法（不超过20字节，只有能由数字、字母和下划线构成）
  * 密码长度不低于6，且不超过32
  * 邮箱合法（不超过32字节，不小于8字节，满足邮箱格式要求）
  * 用户名未被使用
  * 邮箱未被使用
  
  ***由于html中不含javascrip等脚本，因此账户信息的检查由服务器完成，要求账户所有信息明文传输***
5. 数据库设计  
  本站点数据库中包含两张表：  
<table>
  <tr>
    <th>Tables_in_avatar_test</th>
  </tr>
  <tr>
    <td>email2user</td>
  </tr>
  <tr>
    <td>user_info</td>
  </tr>
</table>
  user_info表的结构为：
<table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Null</th>
    <th>Key</th>
    <th>Default</th>
    <th>Extra</th>
  </tr>
  <tr>
    <td>username</td>
    <td>varchar(20)</td>
    <td>NO</td>
    <td>PRI</td>
    <td>NULL</td>
    <td></td>
  </tr>
  <tr>
    <td>password</td>
    <td>char(64)</td>
    <td>NO</td>
    <td></td>
    <td>NULL</td>
    <td></td>
  </tr>
  <tr>
    <td>salt</td>
    <td>char(64)</td>
    <td>NO</td>
    <td></td>
    <td>NULL</td>
    <td></td>
  </tr>
  <tr>
    <td>email</td>
    <td>varchar(32)</td>
    <td>NO</td>
    <td></td>
    <td>NULL</td>
    <td></td>
  </tr>
</table>
  email2user表的结构为：
<table>
  <tr>
    <th>Field</th>
    <th>Type</th>
    <th>Null</th>
    <th>Key</th>
    <th>Default</th>
    <th>Extra</th>
  </tr>
  <tr>
    <td>email</td>
    <td>varchar(32)</td>
    <td>NO</td>
    <td>PRI</td>
    <td>NULL</td>
    <td></td>
  </tr>
  <tr>
    <td>password</td>
    <td>varchar(20)</td>
    <td>NO</td>
    <td></td>
    <td>NULL</td>
    <td></td>
  </tr>
</table>

## Install
1. 首先确保Apache服务器已安装并进行了cgi-bin和静态文件目录的设置，Python2.7及mysql-python已安装
2. 从github上下载
3. 在静态文件目录中创建avatar目录，并修改权限
4. 创建数据库
